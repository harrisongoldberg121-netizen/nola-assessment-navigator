"""Layer 2: look up one property's assessment from public City of New Orleans data.

Steps (all public, no API keys):
  1. Geocode the address with the City's address-point geocoder.
  2. Find the tax bill number(s) at that point with the City's "WhereYa_Taxbill"
     map service (the same service behind nola.gov/find-tax-bill).
  3. Download the official tax bill PDFs from taxbills.nola.gov for the latest
     two years and read the assessment lines on page 1.

Owner names are on the bills but are deliberately NOT returned (CLAUDE.md 3.4).
"""

from __future__ import annotations

import io
import re

import requests
from pypdf import PdfReader

UA = {"User-Agent": "nola-assessment-navigator (student class project)"}
GEOCODER = "https://maps.nola.gov/server/rest/services/Geolocators/AddressPointLocator/GeocodeServer/findAddressCandidates"
TAXBILL_SERVICE = "https://gis.nola.gov/arcgis/rest/services/apps/WhereYa_Taxbill/MapServer/identify"
BILL_PDF = "https://taxbills.nola.gov/pdfs/{year}/{bill}.pdf"
PAY_PAGE = "https://services.nola.gov/service.aspx?load=treasury&type=1&taxbill={bill}"
BILL_YEARS = (2026, 2025)


class LookupError(Exception):
    """Raised with a plain-language message the app can show to the user."""


def _norm(address: str) -> str:
    """Rough address key for comparing '1300 Perdido Street' with '1300 PERDIDO ST'."""
    a = address.upper().split(",")[0]
    for long, short in (("STREET", "ST"), ("AVENUE", "AVE"), ("BOULEVARD", "BLVD"),
                        ("DRIVE", "DR"), ("PLACE", "PL"), ("ROAD", "RD"),
                        ("COURT", "CT"), ("CIRCLE", "CIR"), ("SAINT ", "ST ")):
        a = re.sub(rf"\b{long}\b", short, a)
    a = re.sub(r"\bAV\b", "AVE", a)
    return re.sub(r"[^A-Z0-9]", "", a)


def geocode(address: str) -> dict:
    r = requests.get(GEOCODER, params={"SingleLine": address, "outSR": 4326,
                                       "maxLocations": 1, "f": "json"},
                     headers=UA, timeout=20)
    r.raise_for_status()
    c = (r.json().get("candidates") or [None])[0]
    if not c or c.get("score", 0) < 90:
        raise LookupError("I couldn't find that address in New Orleans. Check the spelling and include the house number, like \"400 Poydras St\".")
    return {"matched": c["address"], "x": c["location"]["x"], "y": c["location"]["y"]}


def tax_bills_at(x: float, y: float) -> list[dict]:
    d = 0.0005
    r = requests.get(TAXBILL_SERVICE, params={
        "geometry": f'{{"x":{x},"y":{y}}}', "geometryType": "esriGeometryPoint",
        "sr": 4326, "layers": "all:1", "tolerance": 1,
        "mapExtent": f"{x - d},{y - d},{x + d},{y + d}", "imageDisplay": "20,20,96",
        "returnGeometry": "false", "f": "json"}, headers=UA, timeout=20)
    r.raise_for_status()
    seen, out = set(), []
    for res in r.json().get("results", []):
        a = res.get("attributes", {})
        bill = a.get("Tax Bill Number")
        if bill and bill not in seen:
            seen.add(bill)
            out.append({"bill": bill, "site": (a.get("Street Address") or "").strip()})
    return out


def _num(pattern: str, text: str) -> float | None:
    m = re.search(pattern, text)
    return float(m.group(1).replace(",", "")) if m else None


def read_bill(bill: str, year: int) -> dict | None:
    url = BILL_PDF.format(year=year, bill=bill)
    r = requests.get(url, headers=UA, timeout=30)
    if r.status_code != 200 or "pdf" not in r.headers.get("content-type", ""):
        return None
    text = PdfReader(io.BytesIO(r.content)).pages[0].extract_text()
    land = _num(r"LAND ASSESSMENT\s*\n\s*([\d,]+)", text)
    impr = _num(r"IMPROVEMENT ASSESSMENT\s*\n[^\n]*?\s([\d,]+)\s*\n", text)
    homestead = _num(r"HOMESTEAD EXEMPTION\s*\n\s*([\d,]+)", text)
    total = _num(r"\$([\d,]+\.\d\d)", text)
    loc = re.search(r"PROPERTY LOCATION\s*\n([^\n]+)", text)
    if land is None and impr is None:
        return None
    return {
        "year": year,
        "location": loc.group(1).strip() if loc else "",
        "land_assessment": land or 0,
        "improvement_assessment": impr or 0,
        "total_assessment": (land or 0) + (impr or 0),
        "homestead_exemption": homestead or 0,
        "total_due": total,
        "pdf_url": url,
    }


def lookup(address: str) -> dict:
    """Return a property summary, or raise LookupError with a friendly message."""
    try:
        g = geocode(address)
        bills = tax_bills_at(g["x"], g["y"])
    except requests.RequestException:
        raise LookupError("The City's address or tax bill service didn't respond. Please try again in a minute.")
    if not bills:
        raise LookupError("I found the address but no tax bill there. It may be a street, a park, or a property that isn't taxed.")

    want = _norm(g["matched"])
    chosen = next((b for b in bills if _norm(b["site"]) == want), bills[0])

    years = []
    for y in BILL_YEARS:
        try:
            b = read_bill(chosen["bill"], y)
        except requests.RequestException:
            b = None
        if b:
            years.append(b)
    if not years:
        raise LookupError(
            "I found the tax bill number but couldn't read the bill. Government, church, and other "
            "fully exempt properties often have no bill. You can check it yourself at nola.gov/find-tax-bill.")

    return {
        "searched": address,
        "matched_address": g["matched"],
        "tax_bill": chosen["bill"],
        "site_address": chosen["site"],
        "other_bills_here": [b["bill"] for b in bills if b["bill"] != chosen["bill"]],
        "years": years,  # newest first
        "pay_page": PAY_PAGE.format(bill=chosen["bill"]),
        "address_match": _norm(chosen["site"]) == want,
    }


def summary_for_model(p: dict) -> str:
    """Plain-text block added to the chatbot's instructions after a lookup."""
    lines = [
        f"Address searched: {p['matched_address']} (tax bill no. {p['tax_bill']}, assessed location: {p['site_address']}).",
        "Source: City of New Orleans tax bills at taxbills.nola.gov [P]. Owner name intentionally not shown.",
    ]
    for y in p["years"]:
        lines.append(
            f"{y['year']} tax bill: land assessment ${y['land_assessment']:,.0f}; improvement assessment "
            f"${y['improvement_assessment']:,.0f}; total assessed value ${y['total_assessment']:,.0f}; "
            f"homestead exemption ${y['homestead_exemption']:,.0f}; total due on bill "
            f"{'$' + format(y['total_due'], ',.2f') if y['total_due'] is not None else 'not read'}. Bill PDF: {y['pdf_url']}"
        )
    if len(p["years"]) == 2:
        a, b = p["years"][0]["total_assessment"], p["years"][1]["total_assessment"]
        if b:
            lines.append(f"Change in total assessed value {p['years'][1]['year']}→{p['years'][0]['year']}: {100 * (a / b - 1):+.1f}%.")
    if not p["address_match"]:
        lines.append("Note: the bill's listed address differs from the searched address; the property may share a parcel with other addresses.")
    return "\n".join(lines)
