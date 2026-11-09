#!/bin/bash
# Match owner addresses to Orleans Parish parcels.
#
# Steps for each address:
#   1. Geocode with the City of New Orleans address-point geocoder (free, no key).
#      If that fails or scores under 90, fall back to the US Census Geocoder.
#   2. Find the parcel polygon at that point (Assessor Landbase "Parcels" layer)
#      -> GEOPIN (parcel ID) and the parcel's site address.
#   3. Look up the parcel's Assessor account IDs (PARID) from "Parcels To Join".
#      PARIDs look like "1300-PERDIDOST". If one matches the geocoded address,
#      the match is EXACT; otherwise it's PARCEL_ONLY (right parcel, but the
#      address is one of several on a large parcel or written differently).
#
# Usage: ./match_addresses.sh test_addresses.csv > match_results.csv
# Needs: bash, curl, jq (all built into macOS).

set -u
IN="${1:-test_addresses.csv}"
UA="nola-assessment-navigator (student class project)"
CITY_GEO="https://maps.nola.gov/server/rest/services/Geolocators/AddressPointLocator/GeocodeServer/findAddressCandidates"
CENSUS_GEO="https://geocoding.geo.census.gov/geocoder/locations/onelineaddress"
PARCELS="https://maps.nola.gov/server/rest/services/Assessor/Landbase_Layers/MapServer/0/query"
PARIDS="https://maps.nola.gov/server/rest/services/Assessor/Parcels_To_Join/MapServer/0/query"

# "1300 Perdido Street, New Orleans" -> "1300-PERDIDOST" (the Assessor's PARID style)
# Learned from test run 1: the Assessor abbreviates Avenue=AV, Boulevard=BL,
# Circle=CR (not the postal AVE/BLVD/CIR).
to_parid() {
  echo "$1" | cut -d, -f1 | tr '[:lower:]' '[:upper:]' | sed -E \
    -e 's/ STREET$/ ST/; s/ AVENUE$/ AV/; s/ BOULEVARD$/ BL/; s/ DRIVE$/ DR/' \
    -e 's/ CIRCLE$/ CR/; s/ HIGHWAY$/ HWY/; s/ PLACE$/ PL/; s/ ROAD$/ RD/' \
    -e 's/ COURT$/ CT/; s/ PARKWAY$/ PKWY/; s/ LANE$/ LN/' \
    -e 's/ SAINT / ST /g' \
    -e 's/^([0-9]+) /\1-/' -e 's/ //g'
}

query_point() {  # $1=url $2=fields $3=x $4=y
  curl -s -m 30 -A "$UA" -G "$1" \
    --data-urlencode "geometry={\"x\":$3,\"y\":$4,\"spatialReference\":{\"wkid\":4326}}" \
    --data-urlencode "geometryType=esriGeometryPoint" --data-urlencode "inSR=4326" \
    --data-urlencode "spatialRel=esriSpatialRelIntersects" --data-urlencode "outFields=$2" \
    --data-urlencode "returnGeometry=false" --data-urlencode "f=json"
}

echo "id,input_address,geocoder,geocode_score,matched_address,lon,lat,geopin,parcel_site_address,parids_on_parcel,status,reason"

tail -n +2 "$IN" | while IFS= read -r line; do
  id=$(echo "$line" | cut -d, -f1)
  addr=$(echo "$line" | sed -E 's/^[0-9]+,"([^"]*)".*/\1/')
  src="city"; score=""; matched=""; x=""; y=""

  # 1. City geocoder
  r=$(curl -s -m 30 -A "$UA" -G "$CITY_GEO" --data-urlencode "SingleLine=$addr" \
      --data-urlencode "outSR=4326" --data-urlencode "maxLocations=1" --data-urlencode "f=json")
  score=$(echo "$r" | jq -r '.candidates[0].score // empty')
  if [ -n "$score" ] && [ "$(echo "$score >= 90" | bc)" = 1 ]; then
    matched=$(echo "$r" | jq -r '.candidates[0].address')
    x=$(echo "$r" | jq -r '.candidates[0].location.x'); y=$(echo "$r" | jq -r '.candidates[0].location.y')
  else
    # 1b. Census fallback
    src="census"
    r=$(curl -s -m 30 -A "$UA" -G "$CENSUS_GEO" --data-urlencode "address=$addr" \
        --data-urlencode "benchmark=Public_AR_Current" --data-urlencode "format=json")
    matched=$(echo "$r" | jq -r '.result.addressMatches[0].matchedAddress // empty')
    x=$(echo "$r" | jq -r '.result.addressMatches[0].coordinates.x // empty')
    y=$(echo "$r" | jq -r '.result.addressMatches[0].coordinates.y // empty')
    score=$([ -n "$matched" ] && echo "match" || echo "")
  fi

  if [ -z "$x" ]; then
    echo "$id,\"$addr\",$src,,,,,,,,NO_MATCH,Neither geocoder could find this address"
    continue
  fi

  # 2. Parcel at that point
  p=$(query_point "$PARCELS" "GEOPIN,SITUS_NUMBER,SITUS_DIR,SITUS_STREET,SITUS_TYPE" "$x" "$y")
  geopin=$(echo "$p" | jq -r '.features[0].attributes.GEOPIN // empty')
  site=$(echo "$p" | jq -r '.features[0].attributes | select(.) | [.SITUS_NUMBER, .SITUS_DIR, .SITUS_STREET, .SITUS_TYPE] | map(select(. != null and . != "")) | map(tostring) | join(" ")')

  if [ -z "$geopin" ]; then
    echo "$id,\"$addr\",$src,$score,\"$matched\",$x,$y,,,,NO_MATCH,Geocoded but no Orleans Parish parcel at that point (outside the parish or in a street)"
    continue
  fi

  # 3. Assessor account IDs on that parcel
  j=$(query_point "$PARIDS" "PARID" "$x" "$y")
  parids=$(echo "$j" | jq -r '[.features[].attributes.PARID] | unique | join("; ")')
  want=$(to_parid "$matched")
  rest="${want#*-}"; near="${want%%-*}-${rest:0:4}"  # house number + first 4 letters of street
  if echo "; $parids;" | grep -q "; $want;"; then
    status="EXACT"; reason="Address matches Assessor account $want"
  elif echo "; $parids" | grep -q "; $near"; then
    status="NEAR"; reason="Same house number and street start ($near...) but spelled differently from $want - check by eye"
  else
    status="PARCEL_ONLY"; reason="Found the parcel, but no account ID equals $want"
  fi
  echo "$id,\"$addr\",$src,$score,\"$matched\",$x,$y,$geopin,\"$site\",\"$parids\",$status,$reason"
  sleep 0.5  # be polite to free public services
done
