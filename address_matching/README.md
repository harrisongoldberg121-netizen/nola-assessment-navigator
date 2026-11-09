# Address matching: owner address → Assessor parcel

**Goal (Layer 2):** a user types their address, and we find their parcel and Assessor account so we can look up their record in the roll data.

**Script:** `match_addresses.sh` (bash + curl + jq; no installs, no API keys)
**Test input:** `test_addresses.csv` (12 addresses) → **Results:** `match_results.csv` (final), `match_results_run1.csv` (first attempt)

## Method
1. **Geocode** the address with the **City of New Orleans address-point geocoder**, which places it on the city's own address points. If the city geocoder returns nothing or scores under 90, **fall back to the US Census Geocoder**.
2. **Parcel lookup:** find the Assessor parcel polygon that contains the point (`Landbase_Layers/Parcels`). This gives the **GEOPIN** (parcel ID) and the parcel's main site address.
3. **Account check:** list the Assessor account IDs (**PARID**) on that parcel (`Parcels_To_Join`). Convert the geocoded address to PARID style (`1300 Perdido Street` → `1300-PERDIDOST`) and compare.
   - **EXACT:** a PARID equals the address. This is the account to look up.
   - **NEAR:** same house number and first 4 letters of the street, but spelled differently. A person should check it.
   - **PARCEL_ONLY:** the parcel was found, but none of its accounts match the address.
   - **NO_MATCH:** the address couldn't be geocoded, or the point isn't on an Orleans Parish parcel.

Test addresses are public buildings and landmarks, not private homes, so no individual's home address is published in this project.

## Results (run 2026-11-08)
| # | Address | Result | Notes |
|---|---|---|---|
| 1 | 1300 Perdido St (City Hall) | EXACT | Parcel 41032325 has 3 accounts. The parcel's main address is 1227 Poydras St, but the account `1300-PERDIDOST` matched. |
| 2 | 225 Morgan St (Algiers Courthouse) | EXACT | West Bank works |
| 3 | 6500 Magazine St (Audubon Zoo) | EXACT | Parcel's main address is 501 Walnut St; account matched |
| 4 | 1 Collins Diboll Cir (NOMA) | **NEAR** | Assessor's record is spelled **"DIBBOLL"**, a typo in the source data |
| 5 | 615 City Park Ave (Delgado) | EXACT | |
| 6 | 726 St Peter St (Preservation Hall) | EXACT | "St" correctly read as "Saint" |
| 7 | 1500 Sugar Bowl Dr (Superdome) | EXACT | |
| 8 | 6823 Saint Charles Avenue (Tulane) | EXACT | Spelled-out "Saint" and "Avenue" handled |
| 9 | 400 Poydras St (office tower) | EXACT | |
| 10 | 5620 Read Blvd (New Orleans East) | EXACT | |
| 11 | 3000 Veterans Memorial Blvd, **Metairie** | NO_MATCH ✔ | Census geocoder found it in Jefferson Parish, but no Orleans parcel is there, so it was correctly rejected. The city geocoder didn't return it. |
| 12 | 99999 Fake St | NO_MATCH ✔ | Neither geocoder found it, so it was correctly rejected |

**Score: 10 of 10 real Orleans addresses found the correct parcel (9 EXACT, 1 NEAR). 2 of 2 invalid addresses were correctly rejected.**

### What failed in the first run, and the fix
Run 1 (`match_results_run1.csv`) had only **6 EXACT**. Four addresses were PARCEL_ONLY because I used US Postal abbreviations. The Assessor writes **AV** (not AVE), **BL** (not BLVD), and **CR** (not CIR). After fixing the abbreviations, 9 were exact. NOMA stayed off because of the Assessor's "DIBBOLL" spelling, so I added the NEAR tier to catch spelling differences like that.

## Limits and next steps
- **Condos and apartments:** unit numbers aren't handled yet. Many condo units share one parcel, so we'd need to match the unit to the right account.
- **Large parcels:** a parcel can have several addresses and accounts (City Hall has 3). Always match on the account, not the parcel's main address.
- **Linking to the roll files:** the 2025/2026 roll files haven't been added yet, so we don't know their key. They may use the PARID, the GEOPIN, or a tax bill number like the permit data's `pin`. Confirm that when the files arrive (see `docs/data_dictionary.md`).
- **Privacy:** the chatbot should only show a record for the address the user typed, and shouldn't display owner names (CLAUDE.md §3.4).
- The city services are free and public. The script waits half a second between addresses to be polite.

## How to run
```bash
cd address_matching
./match_addresses.sh test_addresses.csv > match_results.csv
```
