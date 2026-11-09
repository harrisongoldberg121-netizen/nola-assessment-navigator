#!/bin/bash
# Pull value-changing building permits from the City of New Orleans open data
# portal (Socrata API, dataset rcm3-fn58, "Permits"). No API key needed.
#
# Keeps: new construction, renovations, demolitions, accessory structures
# issued on or after 2023-01-01 (the last reappraisal year, so these are the
# changes since tax-year-2024 values were set).
# Drops personal names: owner, applicant, contractors are NOT downloaded.
#
# Usage: ./fetch_permits.sh   (writes nola_value_permits_2023_on.csv here)

cd "$(dirname "$0")"
OUT="nola_value_permits_2023_on.csv"
curl -s -m 300 -G "https://data.nola.gov/resource/rcm3-fn58.csv" \
  --data-urlencode "\$select=numstring as permit_number, type, code, issuedate, currentstatus, constrval, bldgarea, landuseshort, address, pin, location_1.latitude as latitude, location_1.longitude as longitude" \
  --data-urlencode "\$where=issuedate >= '2023-01-01' AND type in ('New Construction','Renovation (Structural)','Renovation (Non-Structural)','Demolition','Accessory Structure')" \
  --data-urlencode "\$order=issuedate" \
  --data-urlencode "\$limit=100000" \
  -o "$OUT"
echo "Saved $(($(wc -l < "$OUT") - 1)) permits to $OUT on $(date +%F)"
