# CLAUDE.md — NOLA Assessment Navigator

> Instruction file for the coding agent (Claude Code / Cursor). Read this before every task.
> Living document, updated all semester. Last updated: 2026-11-08 (Part 2: data work).
> Facts below were checked against official pages on 2026-11-04. Items still marked **[VERIFY]** could not be confirmed from an official source; see §9.

### Changelog
- **2026-11-08:** Part 2 data work. Added the Zillow ZHVI file (EDA, 5 charts), a data dictionary (`docs/data_dictionary.md`), address matching (`address_matching/`, 10/10 test addresses found), outside data from the city's permits API (`data/outside/`), and 10 test questions (`docs/test_questions.md`). Rewrote §3 and §8, and added data questions to §9.
- **2026-11-04:** Corrected the appeal calendar. Summer 2026 open rolls were for the **2027** tax year (July 15 to Aug 17, 2026; appeals due Aug 20, 2026), not Aug 15/18. Resolved the Louisiana Tax Commission deadline (30 calendar days under LAC 61:V.3103). Replaced homestead, freeze and veteran rules with the Assessor's current requirements. Updated the worked example to the 2026 levy. Replaced general links with specific pages and dropped commercial sites as sources. Added chatbot files (§6).
- **2026-10-21:** First draft.

---

## 1. Purpose

**What it is:** The NOLA Assessment Navigator is an AI assistant that helps New Orleans (Orleans Parish) property owners understand their property assessment, the exemptions they can claim, and how to appeal.

**Who uses it:** Homeowners and small property owners in New Orleans, especially people who:
- just got an assessment notice and don't understand it,
- think their value went up too much,
- don't know whether they have the homestead exemption or other exemptions,
- missed or are worried about missing an appeal deadline.

Assume users are **not** tax experts. Use plain language, short answers, and define terms (e.g., "assessed value") the first time they appear.

**Three layers:**

| Layer | Name | What it answers | Data used |
|---|---|---|---|
| 1 | **General guidance** | How assessment, millage, exemptions, and appeals work in Orleans Parish | Domain knowledge in §2 and the public education content in §5 |
| 2 | **My property** | "What is my property assessed at? Did it change? Do I have homestead?" | 2025 and 2026 assessment rolls (§3), looked up by address or parcel number |
| 3 | **Market context** | "How does my change compare to my neighborhood / similar properties?" | Aggregations across the rolls (by neighborhood, property class, tax district) |

Part 1 of the project builds **Layer 1 only.**

---

## 2. Domain knowledge: how Orleans Parish assessment works

### 2.0 Key idea: Orleans Parish works one year ahead
Values the Assessor sets in a given summer are for the **next** year's tax bill. For example, the rolls open from July 15 to Aug 17, **2026** are the **2027** assessment rolls, which become the tax bills mailed around January **2027**. [3] Always name both the year of the open-rolls period and the tax year.

### 2.1 Who does what
- **Orleans Parish Assessor's Office:** sets the value of every property and handles exemptions and freezes. It does **not** set tax rates, mail bills, or collect taxes. [2]
- **Board of Review (BOR):** the **New Orleans City Council**, which hires real estate professionals to hear appeals. It is independent of the Assessor and can raise or lower a value. It **cannot** change prior-year assessments or decide homestead denials, age freezes, or disability freezes; those stay with the Assessor. [4]
- **Louisiana Tax Commission (LTC):** state body that hears appeals of Board of Review decisions. [7]
- **City of New Orleans Bureau of the Treasury:** sets up and mails tax bills and collects payments. Room 1W40, City Hall, (504) 658-1701. [2]
- **Taxing bodies** (City, School Board, Sewerage & Water Board, levee districts, etc.) set the millage rates. [2][5]

### 2.2 Fair market value (FMV) and mass appraisal
- The Assessor estimates each property's fair market value using a **Computer-Assisted Mass Appraisal (CAMA)** system. The system combines inspection data, land sales, land use, aerial imaging, and maps to value all properties uniformly, instead of appraising each house one at a time. [2]
- Properties are grouped into **assessment neighborhoods**: areas with similar character, even when home size, age, and construction vary. [2]
- Values change with local, regional, and national market changes, and with changes to the property such as damage, demolition, or renovations. [2]

### 2.3 Assessed value
The Louisiana Constitution sets assessed value as a percentage of fair market value: [2]
- **Residential property and all land: 10%**
- **Commercial and industrial buildings: 15%**

Example: a $100,000 home has an assessed value of $10,000. [2]

### 2.4 Millage
- A **mill** is one-tenth of one percent (0.001), or $1 of tax per $1,000 of assessed value. [2]
- **2026 levy:** the citywide total is **121.20 mills**. Add the levee district: **10.79** for East Bank (Orleans Levee District), or **10.81** for West Bank (Algiers Levee District). [5]
  - East Bank total: 121.20 + 10.79 = **131.99 mills**
  - West Bank total: 121.20 + 10.81 = **132.01 mills**
- Some neighborhoods add special district taxes, like the Downtown Development District, so a bill can be higher than these totals. [2]
- **Homestead does not reduce three millages:** Police (4.67), Fire (4.62), and Fire (2.22), which total **11.51 mills** in 2026. [5]
- **Formula:** `Tax = (Assessed value − homestead) × homestead-exempt millage + (Assessed value) × non-exempt millage`

### 2.5 Homestead exemption
- **Who qualifies:** every homeowner in Orleans Parish, for their **primary residence**, meaning the owner lives in it. [1]
- **Amount:** the first **$75,000 of market value** ($7,500 of assessed value) is exempt from most property taxes. [1][5]
- **How to apply:** fill out the application, then attend a virtual or in-person appointment, or walk in at City Hall or the Algiers Courthouse. **Every owner who lives in the home must be present**, including both spouses. [1][2]
- **Documents required:** [1][2]
  1. Completed homestead exemption application
  2. Proof of ownership
  3. Valid Louisiana driver's license or state ID showing the property address
  4. A current Entergy, cable, or landline phone bill in the applicant's name. The service and mailing address must match the property, and it must show normal residential use. Sewerage & Water Board, internet, and Delta bills are **not** accepted.
  5. If you claimed homestead somewhere else, proof that it was cancelled
- **Renewal:** once granted, homestead stays on the property. You don't reapply every year. [13]

### 2.6 Other exemptions and freezes
All of these require the home to already have a homestead exemption. [1]

| Program | Who qualifies | Benefit | Key documents |
|---|---|---|---|
| **Age freeze** (Special Assessment Level) | 65 or older by Dec 31 of the year, household income **$102,700 or less** | Freezes the home's taxable assessment. Once obtained, it is permanent. | ID with property address; prior year's **signed** 1040; Social Security or pension award letter. Bank statements and W-2s are not accepted. |
| **Disability freeze** (Special Assessment Level) | 50–100% disability verified by a federal or state agency, household income **$102,700 or less** | Freezes the taxable assessment | ID; Social Security or VA award letter; prior year's signed 1040 |
| **Disabled veteran exemption** | Service-connected disability of 50% or more | 50–70%: $10,000 total assessed value exempt (homestead $7,500 + $2,500). 70–99%: $12,000 total. 100%: total exemption, except non-homestead millages. | ID; VA-certified property tax benefit form; Entergy bill; VA benefit summary showing the disability % |
| **First responder exemption** | Full-time public safety or public works employee, or volunteer firefighter, with an employer in Orleans Parish | Extra $25,000 off market value ($2,500 assessed) | ID; employment verification letter on official letterhead |

Sources: [1], [2].

- **Freeze deadline:** to get a freeze for the current year, the application must be received **no later than three business days after the rolls close**. [2]
- **Freeze "tax trap" (2026 news):** in Orleans Parish, a frozen assessment stays frozen even if the home's market value **drops**, so some freeze owners pay more than they would without it. The Assessor's current policy is that owners must **waive and reapply** to get the lower value, which means income-qualifying again. In June 2026 the Assessor asked the Louisiana Attorney General for a legal opinion. As of Aug 10, 2026, none had been issued. [11] **[VERIFY whether the AG has ruled]**

### 2.7 Reassessment cycle and the 2027 reassessment
- The Louisiana Constitution requires the Assessor to revalue all property **at least once every four years**. Extra reappraisals can happen after major events, as after Hurricane Katrina. [2]
- The last parishwide reappraisal was for **tax year 2024**. [10] Four years later, the next is for **tax year 2028**. Because Orleans works one year ahead (§2.0), the new values should appear when rolls open in **summer 2027**. The exact 2027 open-roll dates have not been announced. [2][10]
- **Millage rollback and roll forward:** after a reappraisal, taxing bodies must adjust millage rates so a reappraisal alone doesn't raise total revenue (the "rollback"). A taxing body can then vote by **two-thirds**, after a **public hearing**, to raise the rate back up to the prior year's maximum (a "roll forward"). This does not apply to millages that pay off bonds. [9]
- **What it means for owners:** a higher value doesn't automatically mean a higher bill, because rates are rolled back. Bills can still rise if your value rose more than average, or if taxing bodies roll forward. Homestead and freezes still apply. [2][9]

### 2.8 Appeal process and deadlines (2026 cycle, for tax year 2027)
| Step | What happens | 2026 dates (TY2027) | Source |
|---|---|---|---|
| 1. Open rolls | View your value at nolaassessor.com, or meet with appraisal staff online or in person. Book at least 24 hours ahead by calling (504) 754-8811 or online. Walk-ins are seen first come, first served. | **July 15 – Aug 17, 2026**, Mon–Fri, 8:30 a.m.–4 p.m. | [3] |
| 2. File a Board of Review appeal | Online at nolaassessor.com, **or** by hand or mail with **4 copies** of the BOR form and all supporting materials. Missing documents mean the appeal is denied as incomplete. | Online: July 22 – **4 p.m. Aug 20, 2026** | [3][4] |
| 3. BOR hearing | Hearing notice mailed before Sept 15. Hearings held at Delgado Community College, City Park Campus, Student Life Center. | **Sept 15 – 25, 2026** | [4] |
| 4. BOR decision | Written decision sent by certified mail | Beginning week of **Oct 19, 2026** | [4] |
| 5. Appeal to Louisiana Tax Commission | File **LTC Form 3103.A** and attach a copy of the BOR decision. You can file by certified or registered mail or online at the LTC website. Evidence given to the Assessor or BOR must be **resubmitted**. | **30 calendar days** from the earlier of when the BOR decision is sent or delivered | [7][12] |
| 6. District court | Appeal an LTC decision to district court | Within **30 days** of the LTC decision | [8] |

- **General rule:** rolls close **Aug 15**, or the following Monday if Aug 15 falls on a weekend. BOR appeals and freeze applications are due **three business days** after the rolls close. [2] In 2026, Aug 15 was a Saturday, so the rolls closed Monday, Aug 17 and appeals were due Thursday, Aug 20. [3]
- **LTC deadline conflict:** the City Council page says **10 business days** after the BOR notice. [4] The current official LTC rule, LAC 61:V.3103(B)(1), last amended March 2025, says **30 calendar days**. [7] Follow the state rule, but tell owners that filing within 10 business days satisfies both.
- **Evidence that helps:** a recent appraisal, a builder's contract, insurance documents, recent printed and dated photos, contractor repair estimates, the property's recent sale price, recent sales of similar nearby homes, and a real estate professional's opinion of value. [2][4]
- **What an appeal is not:** you appeal because you believe the **value** is wrong, for example the square footage is off or similar homes sold for less. You don't appeal because taxes feel too high; that is up to the taxing bodies. [2]
- **Missed the deadline?** The BOR can't change prior-year assessments. [4] For the 2027 tax year, the window closed Aug 20, 2026. The next chance is during summer 2027 open rolls, for tax year 2028.

### 2.9 Tax bills
- **2026 bills:** posted online at nola.gov/find-tax-bill and mailed by the end of January 2026. They were due **Feb 28, 2026**, with interest of **1% per month** after that. [6]
- **Paying:** by mail (check, money order, or cashier's check; no cash), or online (e-check is free; cards carry a 2.49% fee). Partial payments are not accepted. [6]
- The due date is set each year. The 2027 date had not been announced as of Nov 4, 2026. **[VERIFY each January]**

### 2.10 Sources (specific pages, checked 2026-11-04)
1. Orleans Parish Assessor, **Homestead & SAL** (requirements for homestead, freezes, veteran and first responder exemptions): https://www.nolaassessor.com/homestead-sal/
2. Orleans Parish Assessor, **FAQ** (mass appraisal, assessment percentages, millage, appeals, homestead and freeze filing, deadlines rule, Treasury contact): https://www.nolaassessor.com/faq/
3. Orleans Parish Assessor, **"2027 Assessment Rolls Open for Public Inspection July 15 to August 17"** (July 13, 2026): https://www.nolaassessor.com/2026/07/13/2027-assessment-rolls-open-for-public-inspection-july-15-to-august-17/
4. New Orleans City Council, **Property Tax Assessments & Appeals** (Board of Review role, 2026 hearing calendar, evidence): https://council.nola.gov/resources/property-tax-assessments-and-appeals/
5. City of New Orleans Treasury, **How Taxes Are Calculated** (2026 millage levy table, homestead amount): https://nola.gov/next/treasury/topics/how-taxes-are-calculated/
6. City of New Orleans, **2026 Property Tax Bills announcement** (Jan 25, 2026): https://nola.gov/next/mayors-office/news/articles/january-2026/2026-01-25-city-of-new-orleans-2026-property-tax/
7. Louisiana Administrative Code **61:V.3103**, Appeals to the Louisiana Tax Commission: https://www.law.cornell.edu/regulations/louisiana/La-Admin-Code-tit-61-SS-V-3103
8. **La. R.S. 47:1989** (Tax Commission decisions; appeal to district court): https://legis.la.gov/legis/Law.aspx?d=101446
9. Louisiana Legislative Auditor, **Setting Millage Rates (2026 guide)** (rollback and roll forward): https://lla.la.gov/go/SettingMillageRatesBook2026pdf/$File/LLAsettingMillageRates2026-v01.pdf
10. Louisiana Legislative Auditor, **TY2024 Quadrennial Reappraisal** report: https://lla.la.gov/publicreports.nsf/0/f74bf8c6ffebdf7f86258a8d00657f6c/$file/000037d0b.pdf
11. Verite News, **"Tax mix-up leaves senior, disabled homeowners overcharged and confused"** (Aug 10, 2026): https://veritenews.org/2026/08/10/assessors-office-tax-freeze-homeowners/
12. Louisiana Tax Commission **Form 3103.A** (BOR-to-LTC appeal form, hosted by the City Council): https://council.nola.gov/council/media/Assets/Tax-Assessments/Form-3103A-Updated-for-2017.pdf
13. Orleans Parish Assessor, flyer **"Homestead Exemption: Once Gained, Permanently Applied"** (2021): https://www.nolaassessor.com/wp-content/uploads/sites/80/2023/01/2021-homestead-exempt-flyer_071221.pdf

**Source priority:** official sources (Assessor, City, City Council, LTC, Louisiana law and rules) come first, then the Legislative Auditor, then news. Don't use commercial sites such as appeal services or "assessor search" lookalike sites. If official sources conflict, follow the state law or rule, mention the conflict, and give the safest reading.

---

## 3. Data

Full field definitions are in **`docs/data_dictionary.md`**. Keep it updated whenever a dataset is added or a field is figured out.

### 3.1 Files
| File | What it is | Location | Status |
|---|---|---|---|
| `Zip_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv` | Zillow Home Value Index by ZIP, monthly, Jan 2000 – Sep 2026, all US ZIPs (116.6 MB, from the instructor) | Kept outside the repo (too large); path noted in data dictionary | ✅ loaded |
| `orleans_zhvi_long.csv` | Zillow values for the 17 Orleans ZIPs, one row per ZIP per month | `data/clean/` | ✅ |
| `orleans_zip_summary.csv` | One row per Orleans ZIP: Sep 2026 value, change since Jan 2023, Katrina change, peak | `data/clean/` | ✅ |
| `zhvi_median_us_la_orleans.csv` | Monthly median ZIP value for US, Louisiana, Orleans | `data/clean/` | ✅ |
| `nola_value_permits_2023_on.csv` | City building permits that change property value, 2023 on (outside data, via API) | `data/outside/` | ✅ see its README |
| 2025 assessment roll | Assessor roll | `data/raw/` | **TODO: not received yet** |
| 2026 assessment roll | Assessor roll | `data/raw/` | **TODO: not received yet** |

### 3.1a What the Zillow EDA found (for Layer 3, market context)
EDA page: https://claude.ai/artifact/RvuZQtX8DwRw1f2tDU6gr9 (5 charts).
- **All 17 Orleans ZIPs are worth less than in Jan 2023**, when the last reappraisal's values (TY2024) were being set: from −5.3% (70124 Lakeview) to −27.1% (70113 Central City). Most ZIPs peaked in mid-2022. *Verified by hand from the raw CSV.*
- New Orleans prices rose faster than the US in the 2010s. Year-over-year change turned negative in early 2023, while the US stayed positive. In Sep 2026, Orleans was −3.3% for the year and the US +3.0%.
- In Sep 2026 the typical value ranges from about $152K (70126) to $525K (70115).
- **Katrina:** from Aug 2005 to Aug 2007, flooded ZIPs (70122, 70124, 70125, 70129, 70119, 70128) fell 21–34%, while dry ZIPs (70130, 70114, 70131, 70116) rose 9–15%.
- **What it means for the project:** the 2027 reappraisal (TY2028) may lower many market values. Owners with an age or disability freeze in falling ZIPs may be paying on a frozen value above market (§2.6, the freeze tax trap).
- **Caution:** Zillow's index is a typical middle-tier home in the ZIP, not any property's assessed value. Never use it to tell a user what their home "should" be assessed at (rule 4.3).

### 3.1b Address matching (Layer 2)
Method, results and how to run: `address_matching/README.md`. In short: (1) geocode with the City's address-point geocoder, falling back to the US Census geocoder; (2) find the parcel at that point in the Assessor's GIS layer to get the **GEOPIN**; (3) compare the address with the parcel's Assessor account IDs (**PARID**, e.g. `1300-PERDIDOST`). Tested on 12 addresses: **10/10 real addresses found (9 exact, 1 near-match from an Assessor typo); 2/2 invalid addresses rejected.** The Assessor abbreviates **AV / BL / CR**, not AVE / BLVD / CIR.

### 3.2 What we know so far about the roll files
- Source: Orleans Parish Assessor's Office **[TODO: exact download URL and date pulled]**
- Format / size: **[TODO: CSV/XLSX? number of rows?]**
- Expected fields (confirm once files are opened):
  - Parcel / assessment ID (the key for joining 2025 ↔ 2026)
  - Owner name, mailing address
  - Property (situs) address
  - Property class (residential, commercial, etc.)
  - Land value, building/improvement value, total FMV
  - Assessed value(s)
  - Homestead / special assessment / other exemption flags
  - Tax district (East Bank vs. West Bank)
  - Neighborhood or ward
- **[TODO]** Actual column names and definitions. Fill in a table once the files are loaded.

### 3.3 Known issues / questions
- **[TODO]** Which key do the rolls use: PARID, GEOPIN, or the tax bill number (the permits' `pin`)? This decides how address matching and permits join to the roll.
- **[TODO]** Do parcel IDs match exactly between years?
- **[TODO]** Are values FMV, assessed, or both?
- **[TODO]** Missing values, duplicate parcels, condo units, exempt properties.
- **[TODO]** Confirm whether "2025 roll" and "2026 roll" are named by **tax year** or by the year the rolls were open (§2.0). This changes how we describe them.
- Neither year is a reappraisal year (the last was TY2024), so most values should match. Large changes likely mean new construction, renovation, damage, or corrections.

### 3.4 Data rules for the agent
- Never edit files in `data/raw/`. Write cleaned files to `data/clean/`.
- Owner names are public record but are personal data: don't display owner names in the chatbot unless the user searches their own address.
- Always say which roll year a number comes from.
- Don't download names of owners, applicants, or contractors from outside data unless a feature needs them.
- Test address matching with public buildings, not private homes.
- No Python on the development Mac yet. Data work so far used `sqlite3`, `awk`, `curl` and `jq`, which are built into macOS. The chatbot's Python runs on Streamlit Cloud.

---

## 4. Rules for the chatbot (system-prompt instructions)

When building the chatbot, include these rules in its system prompt:

1. **Cite a source for every fact.** Every factual claim (numbers, deadlines, eligibility rules) must cite a numbered source from §2.10, or the roll data in §3, and link to that page. If no source supports it, don't say it.
2. **Say "I don't know" when unsure.** If the question is outside your sources, or a fact is marked [VERIFY], say so plainly. For example: "I'm not sure about that. Please check with the Assessor's Office." Never guess a deadline, dollar amount, or eligibility rule.
3. **No legal or tax advice.** Explain how the system works in general. Do not tell a user whether they *should* appeal, what their property is "really" worth, or how to file their taxes. Use phrasing like "Many owners in this situation…" or "You may want to talk to…".
4. **Offer a human contact.** End any answer about a specific property, appeal, exemption, or bill with the right office:
   - **Values, appeals, exemptions, freezes:** Orleans Parish Assessor's Office, (504) 754-8811. East Bank: City Hall, 1300 Perdido St. West Bank: 225 Morgan St, (504) 368-7642. Book appointments at nolaassessor.com. [1][3]
   - **Board of Review hearings and decisions:** New Orleans City Council, (504) 658-1080, councilcentralstaff@nola.gov. [4]
   - **Tax bills and payments:** Bureau of the Treasury, (504) 658-1701, Room 1W40, City Hall. [2]
   - **General city questions:** NOLA 311, call 311 or (504) 539-3266. [5]
5. **Disclose it's a student prototype.** First message and footer must say: *"This is a student prototype built for a class project. It is not an official government tool and may contain errors. Always confirm with the Orleans Parish Assessor's Office."*
6. **Plain language.** Aim for an 8th-grade reading level. Define terms. Keep answers short; use bullets for steps.
7. **Dates matter.** Always say which year a deadline applies to, and whether you mean the year rolls were open or the tax year (§2.0). For future years, say the dates are expected, not announced.
8. **Stay in scope.** Orleans Parish only. If asked about another parish, say it's out of scope.

---

## 5. Public education outline (City of New Orleans)

### 5.1 How property values are set
- The Assessor uses mass appraisal (CAMA) and assessment neighborhoods. Values follow market changes and changes to the property. They are reviewed at least every 4 years. Orleans works one year ahead.
- **Sources:** [2], [3], [10]
- **Likely questions:**
  1. Why did my value go up when I didn't change anything?
  2. Does the Assessor come inside my house?
  3. Why is my value different from what Zillow says?

### 5.2 From assessed value to tax bill (worked example)
- Market value → assessed value (10%) → minus homestead → × millage. Homestead doesn't reduce the police and fire millages.
- **Worked example:** a $300,000 East Bank home with homestead, 2026 levy. [2][5]

| Step | Calculation | Result |
|---|---|---|
| Fair market value | — | $300,000 |
| Assessed value (10%) | $300,000 × 0.10 | $30,000 |
| Taxable value after homestead | $30,000 − $7,500 | $22,500 |
| Homestead-exempt millages (131.99 − 11.51 = 120.48 mills) | $22,500 × 0.12048 | $2,710.80 |
| Police and fire millages (11.51 mills, no homestead) | $30,000 × 0.01151 | $345.30 |
| **Estimated 2026 tax** | $2,710.80 + $345.30 | **$3,056.10** |
| Same home without homestead | $30,000 × 0.13199 | $3,959.70 |
| **Homestead savings** | $3,959.70 − $3,056.10 | **$903.60** |

  Special district taxes, like a security district, would be added on top. The Assessor's online Tax Estimator gives an estimate for a specific address. [2]
- **Likely questions:**
  1. What is a mill?
  2. How much will homestead save me?
  3. When is my tax bill due? (2026 bills were due Feb 28, 2026; 1%/month interest after. [6])

### 5.3 Exemptions and how to apply
- Homestead: who qualifies, documents, appointment, every owner present. Age freeze, disability freeze, disabled veteran, and first responder: who qualifies, the $102,700 income limit, deadlines. The freeze "tax trap" when values drop.
- **Sources:** [1], [2], [11]
- **Likely questions:**
  1. How do I know if I already have homestead? (Check your property record on the Assessor's Property Search, or call (504) 754-8811.)
  2. What documents do I need to apply?
  3. I'm over 65. Can my assessment be frozen?

### 5.4 What the 2027 reassessment means
- Next reappraisal is for tax year 2028, with values released at summer 2027 open rolls. Rollback and roll forward. Homestead and freezes still apply. Check your value and appeal during open rolls.
- **Sources:** [2], [9], [10]
- **Likely questions:**
  1. Will my taxes go up in 2028?
  2. When will I find out my new value?
  3. What can I do now to prepare? (Make sure your homestead and any freeze are on file, and keep records like appraisals, repair estimates, and photos.)

### 5.5 How to appeal: where to go and deadlines
- Open rolls → Board of Review (City Council) → Louisiana Tax Commission → district court. Use the 2026 calendar from §2.8, the 3-business-days rule, and the list of helpful evidence.
- **Sources:** [2], [3], [4], [7], [8], [12]
- **Likely questions:**
  1. How do I appeal, and is it free? (No fee is listed on the Assessor's or Council's pages. **[VERIFY]**)
  2. What evidence should I bring?
  3. I missed the deadline. What now?

---

## 6. Draft chatbot (Layer 1)

- **Live link:** https://nola-assessment-navigatorhg.streamlit.app (deployed 2026-11-08; code: https://github.com/harrisongoldberg121-netizen/nola-assessment-navigator)
- **Built with:** Python + Streamlit, hosted free on Streamlit Community Cloud. AI model: Google Gemini (`gemini-3.8-flash`, free tier) via the `google-genai` SDK.
- **Files:** `app.py` (the chatbot), `requirements.txt` (packages), `DEPLOY.md` (how to put it online).
- **Knowledge base:** `app.py` reads §2, §4 and §5 of *this file* at startup and puts them in the model's system prompt. **Editing this file changes what the chatbot knows.** Keep the section headings (`## 2.`, `## 4.`, `## 5.`) as they are, or update `extract_section` in `app.py`.
- **Shows sources in answers:** yes. The system prompt requires numbered citations and a "Sources:" list (rule 4.1).
- **Secrets:** the Gemini API key lives only in Streamlit Cloud → Settings → Secrets as `GEMINI_API_KEY`. Never commit it.
- **Limits:** 30 questions per browser session; only the last 10 messages are sent with each question. Free-tier inputs may be used by Google to improve its products, so the app tells users not to enter personal info.

---

## 7. Sample questions and answers

**Part 2 test set (10 questions with expected answers): `docs/test_questions.md`.** It covers facts (Q1–7) and rules (Q8 no advice, Q9 out of scope, Q10 prototype disclosure). Fill in "How it did" once the chatbot is live. The Part 1 table below is kept for reference.

| # | Question | Chatbot answer (summary or screenshot) | Sources shown? | What it got wrong / missed |
|---|---|---|---|---|
| 1 | How is my property tax calculated in New Orleans? | **[TODO]** | | |
| 2 | How do I apply for the homestead exemption? | **[TODO]** | | |
| 3 | What's the deadline to appeal my assessment? | **[TODO]** | | |
| 4 | What does the 2027 reassessment mean for me? | **[TODO]** | | |
| 5 | I'm 70. Can my assessment be frozen? | **[TODO]** | | |

**What to check in each answer:** Did it cite specific pages? Did it use the corrected 2026 dates (Aug 17 and Aug 20, not Aug 15 and Aug 18)? Did it give $3,056 for the worked example, not $2,970? Did it give the 30-day LTC rule? Did it name a contact? Did it invent anything?

Screenshots: `docs/screenshots/q1.png` … `q5.png` **[TODO]**

**Short note on errors:** **[TODO]**

---

## 8. Working rules for the coding agent

- Project layout:
  - `app.py`, `requirements.txt`, `DEPLOY.md`: the chatbot
  - `data/raw/`: original files, never edited (roll files go here)
  - `data/clean/`: derived data
  - `data/outside/`: outside data + fetch script + README
  - `address_matching/`: matching script, test addresses, results, README
  - `docs/`: data dictionary, test questions, screenshots
- Keep facts in this file; don't hard-code facts in the chatbot that aren't in §2/§5.
- When you add a new fact, add its source to §2.10 at the same time, and link the specific page, not a homepage.
- Ask before deleting or overwriting data files.
- Update this file when we learn something new about the data or domain, and add a line to the Changelog.

---

## 9. Open questions / VERIFY list

**Resolved on 2026-11-04:**
- ~~LTC appeal deadline~~: 30 calendar days (LAC 61:V.3103). The Council page's 10 business days is noted as a conflict. [7][4]
- ~~2026 appeal calendar~~: open rolls July 15 – Aug 17, 2026; online appeals until Aug 20, 2026. [3]
- ~~Board of Review is the City Council~~: confirmed. [4]
- ~~Homestead documents and process~~: confirmed. [1][2]
- ~~Which millages homestead doesn't reduce~~: Police and fire, 11.51 mills in 2026. [5]
- ~~Millage rate and West Bank rate~~: 131.99 (East Bank) and 132.01 (West Bank) for 2026. [5]
- ~~Freeze income limit~~: $102,700. [1][11]
- ~~Disabled veteran amounts~~: confirmed. [1]
- ~~2026 tax bill due date~~: Feb 28, 2026. [6]
- ~~Phone numbers~~: confirmed. [1][2][3][4]
- ~~Commercial assessment percentage~~: 15% for commercial and industrial buildings. [2]
- ~~Rollback and roll forward~~: confirmed. [9]

**Still open:**
1. Has the Attorney General issued the opinion on freezes when values drop? [11]
2. Exact open-roll dates for summer 2027 (the TY2028 reappraisal). Expect an announcement around July 2027.
3. The 2027 tax bill due date (announced each January).
4. Whether any fee applies to a BOR or LTC appeal. None is listed.
5. A 2026 bill (HB 521) to amend the roll-forward rule, La. Const. art. VII §23(C). Did it pass and go to voters?
6. Restoration Tax Abatement and other programs that are less relevant to homeowners.

**Data questions (from `docs/data_dictionary.md`):**
7. Zillow file name: what does `uc` mean? Is the tier the 33rd–67th percentile (file name) or the 35th–65th (Zillow's page)?
8. Zillow `SizeRank`: ranked by what, and why do ranks repeat and skip?
9. Is the permits `pin` the same as the roll's account number? (It matches tax bill numbers.)
10. Official list of permit `landuseshort` codes.
11. Census ACS by ZIP needs a free API key. Sign up to add median income and owner-occupancy. Retry the FEMA flood claims API, which was down on 2026-11-08.
