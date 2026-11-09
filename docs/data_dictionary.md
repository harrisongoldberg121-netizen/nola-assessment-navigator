# Data dictionary

Last updated 2026-11-08. Covers every dataset the project uses so far.

---

## 1. Zillow Home Value Index (ZHVI), by ZIP code

**File:** `Zip_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv` (provided by the professor; 116.6 MB; kept outside the repo because of its size)
**Publisher:** Zillow Research, https://www.zillow.com/research/data/
**Shape:** 26,265 rows (one per US ZIP code), 330 columns (9 descriptive + 321 monthly values)
**Time span:** Jan 2000 – Sep 2026, monthly
**Orleans Parish:** 17 ZIP codes. Extract saved as `data/clean/orleans_zhvi_long.csv` (one row per ZIP per month).

### What the file name means
| Part | Meaning | Confidence |
|---|---|---|
| `Zip` | One row per ZIP code | Confirmed: every row has RegionType = `zip` |
| `zhvi` | Zillow Home Value Index: "a measure of the typical home value" | Confirmed (Zillow Research page) |
| `uc` | Unknown. Possibly a Zillow internal code. | **Not figured out** |
| `sfrcondo` | All homes: single-family residences + condos/co-ops | Confirmed (Zillow: "ZHVI All Homes (SFR, Condo/Co-op)") |
| `tier_0.33_0.67` | Middle tier: homes between the 33rd and 67th percentile of value | Partly. Zillow's page says 35th–65th (see open questions). |
| `sm_sa` | Smoothed and seasonally adjusted | Confirmed (Zillow lists "Smoothed, Seasonally Adjusted") |
| `month` | Monthly values | Confirmed |

### Columns
| Field | Type | Meaning | Notes from checking the data |
|---|---|---|---|
| `RegionID` | integer | Zillow's internal ID for the ZIP | Unique per row. Not a government code; don't join on it. |
| `SizeRank` | integer | Zillow's rank of the region by size (0 = largest) | Ranges 0–33,010, but only 15,482 distinct values across 26,265 rows, so ranks repeat and skip numbers. What "size" means is unclear (see open questions). |
| `RegionName` | text (5 digits) | The ZIP code | Leading zeros are kept (e.g., `08701`). **Read it as text**, or Excel turns `08701` into `8701`. |
| `RegionType` | text | Geography level | Always `zip` in this file |
| `StateName` | text | State | Holds the 2-letter abbreviation (e.g., `LA`), the same as `State`, despite the name |
| `State` | text | State, 2-letter abbreviation | 51 values (50 states + DC) |
| `City` | text | City the ZIP is assigned to | Blank for 7 ZIPs. All 17 Orleans ZIPs say `New Orleans`. |
| `Metro` | text | Metro area (Core-Based Statistical Area) name | Blank for 4,709 rural ZIPs. Orleans: `New Orleans-Metairie, LA`. Contains commas, so it's quoted in the CSV. |
| `CountyName` | text | County, or parish in Louisiana | Never blank. Filter on `Orleans Parish` for this project. |
| `1/31/00` … `9/30/26` | number (US dollars) | ZHVI for that month: the typical value of a middle-tier home, smoothed and seasonally adjusted | Column names are the **last day of the month** in M/D/YY format. Values are in **nominal dollars** (not adjusted for inflation) with many decimals; round for display. Blank means no estimate that month. |

### Missing values (Orleans Parish)
- **Late starts:** 70117 (Bywater / Lower Ninth Ward) begins Nov 2014. 70126 and 70127 (New Orleans East) begin Aug 2010.
- **Hurricane Katrina gaps:** flooded ZIPs are missing some months in 2006: 70122 (Apr–Aug), 70128 (May–Aug), 70119 (Jul–Aug), 70125 (Apr), 70129 (Jun).
- Since Nov 2014, all 17 ZIPs have values every month. **Compare ZIPs over time only from 2014-11 on**, or limit the comparison to ZIPs that existed in both periods.

### How this differs from the Assessor's values
ZHVI is **not** the Assessor's fair market value. It is Zillow's model estimate of a *typical middle-tier home in the ZIP*, not a specific property. It also uses a different date and method than the Assessor's mass appraisal. Use it for **market context (Layer 3)**, not to say what a specific home "should" be assessed at.

---

## 2. Orleans Parish parcels (Assessor GIS, used for address matching)

**Services (ArcGIS REST, public, no key):**
- Parcels: https://maps.nola.gov/server/rest/services/Assessor/Landbase_Layers/MapServer/0 (151,255 parcels; described as maintained by the Assessor's office and updated weekly)
- Parcels To Join: https://maps.nola.gov/server/rest/services/Assessor/Parcels_To_Join/MapServer/0 (also on the open data portal as `pzqp-4ri7`)
- City geocoder: https://maps.nola.gov/server/rest/services/Geolocators/AddressPointLocator/GeocodeServer

| Field | Layer | Meaning | Notes |
|---|---|---|---|
| `GEOPIN` | both | Parcel ID for the land polygon | Integer, e.g. `41032325`. One parcel can hold several accounts. |
| `PARID` | Parcels To Join | Assessor account ID, built from the address | Format `<number>-<STREET><TYPE>` with spaces removed, e.g. `1300-PERDIDOST`. Uses Assessor abbreviations: **AV** (Avenue), **BL** (Boulevard), **CR** (Circle), ST, DR. Spelling follows Assessor records, including typos (e.g., `COLLINSDIBBOLLCR`). |
| `SITUS_NUMBER`, `SITUS_DIR`, `SITUS_STREET`, `SITUS_TYPE` | Parcels | The parcel's main site address, split into parts | On large parcels, this is only one of several addresses. City Hall's parcel is listed as 1227 Poydras St. |
| `ACRES`, `PERIMETER`, `Shape_Area`, `Shape_Length` | Parcels | Parcel size | Coordinates are Louisiana State Plane South (feet); request `outSR=4326` for lat/lon. |

---

## 3. Building permits (City of New Orleans open data, outside data)

**File:** `data/outside/nola_value_permits_2023_on.csv`. See `data/outside/README.md` for details.

| Field | Meaning | Notes |
|---|---|---|
| `permit_number` | City permit number | e.g., `22-22185-RNVS`. The prefix is the filing year; the suffix matches `code`. |
| `type` | Permit type | We kept: New Construction, Renovation (Structural), Renovation (Non-Structural), Demolition, Accessory Structure |
| `code` | Short code for `type` | NEWC (new construction), RNVS (structural renovation), RNVN (non-structural renovation), DEMO (demolition), ACCS (accessory structure) |
| `issuedate` | Date the permit was issued | ISO timestamp |
| `currentstatus` | Permit status | Most common: Permit Issued (7,969), Finaled (4,106), Certificate of Occupancy (2,219). 87 were voided by the applicant. |
| `constrval` | Declared construction value (USD) | Self-reported by the applicant. 1,062 rows are 0. |
| `bldgarea` | Building area (sq ft) | Often 0 or blank |
| `landuseshort` | Land use code | RSFD = single-family, RSF2 = two-family, COMM = commercial, RMF = multifamily, PLEX, MIXD, etc. Full code list not found. |
| `address` | Site address | No ZIP code |
| `pin` | Assessor account / tax bill number | e.g., `614303512`. Matches tax bill file names on taxbills.nola.gov. 787 blank; some hold several numbers (up to 250 characters). |
| `latitude`, `longitude` | Location | No blanks |

Personal names (owner, applicant, contractors) are in the source but were **deliberately not downloaded**.

---

## Open questions (couldn't figure out)
1. **`uc` in the Zillow file name.** It isn't explained on Zillow's data page.
2. **Percentile range.** The file name says 0.33–0.67, but Zillow's page says the 35th–65th percentile. Which is right for this file?
3. **`SizeRank`.** Size by what measure (population, households, homes)? And why does the maximum (33,010) exceed the row count, with repeated ranks?
4. **Revisions.** Zillow upgraded the full ZHVI history in Jan 2023 ("neural Zestimate"). Do older downloads match this file for past months? Our numbers may not match a classmate's older copy.
5. **ZIP vs ZCTA.** Zillow's ZIP boundaries may differ from Census ZCTAs and from neighborhoods. Some ZIPs (70112, 70113, 70119) straddle very different areas.
6. **Assessor account ID vs tax bill `pin`.** Is the permit `pin` the same number as the Assessor roll's account number? It looks like the tax bill number. Confirm once we have the 2025 and 2026 roll files.
7. **Permit land-use codes.** No official list of `landuseshort` codes found yet.
