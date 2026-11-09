# Outside data: City of New Orleans building permits

**Saved file:** `nola_value_permits_2023_on.csv` (15,271 rows, 2.9 MB, pulled 2026-11-08)
**How it was pulled:** `fetch_permits.sh`, using the Socrata Open Data API (SODA) and a filtered query. No API key needed.
**Source:** City of New Orleans open data portal, dataset **"Permits"** (`rcm3-fn58`): https://data.nola.gov/d/rcm3-fn58
Publisher's description: "City of New Orleans permit data starting from 1/01/2012; Updated nightly." The full dataset has 350,045 permits.

## Why this dataset
The Assessor's values change between reappraisals mainly because of **changes to the property**: new construction, renovations, and demolitions (CLAUDE.md §2.2). Permits are the public record of those changes. They can help the chatbot answer "Why did my value change when the market didn't?" (Layer 2), and show which areas are being rebuilt (Layer 3).

## What was kept
- **Permit types:** New Construction (1,629), Renovation (Structural) (2,974), Renovation (Non-Structural) (7,837), Demolition (819), Accessory Structure (2,011).
- **Issued** on or after **2023-01-01**. Tax year 2024 was the last reappraisal (its values were set in 2023), so these are the property changes since then.
- **By year:** 2023: 4,439 · 2024: 4,626 · 2025: 4,038 · 2026 (through Nov 8): 2,167
- **Declared construction value:** about $4.4 billion in total. New construction is $1.59B, and structural renovations are $1.48B.
- **Columns:** see `docs/data_dictionary.md` §3.
- **Not downloaded:** owner, applicant, and contractor names, to follow the project's privacy rule.

## Quality notes
- `constrval` is declared by the applicant and is 0 for 1,062 permits. Treat it as rough.
- `pin` is blank for 787 permits, and some rows list several pins.
- `pin` appears to be the tax bill / Assessor account number: `https://taxbills.nola.gov/pdfs/2026/<pin>.pdf` returns a bill. That would let us join permits to the roll data. **Confirm when the roll files arrive.**
- There's no ZIP code column. Use latitude/longitude, or the address-matching script, to place permits in ZIPs or parcels.
- The data refreshes nightly, so re-running the script will give slightly different counts.

## How to refresh
```bash
cd data/outside
./fetch_permits.sh
```

## What we tried first
1. **US Census ACS API** (median home value and income by ZIP): it now requires an API key and redirects to `missing_key.html`. Sign up for a free key at https://api.census.gov/data/key_signup.html to use it later.
2. **FEMA OpenFEMA flood insurance claims:** the API was returning a "technical difficulties" page on 2026-11-08. Worth retrying: flood claims by ZIP would pair well with the Katrina chart in the EDA.
