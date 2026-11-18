# NOLA Assessment Navigator: Project Summary

**Live prototype:** https://nola-assessment-navigatorhg.streamlit.app · **Code:** https://github.com/harrisongoldberg121-netizen/nola-assessment-navigator · *Student prototype, not an official tool.*

## What the tool does
The Navigator is a chatbot that helps New Orleans property owners understand their property taxes. It works in two layers:
- **Layer 1, general guidance:** answers questions about how assessments, millage, exemptions (homestead, age and disability freezes, veterans), appeals, and deadlines work in Orleans Parish. Answers come only from 13 official sources (Assessor, City, City Council, Louisiana Tax Commission rules, Legislative Auditor). Each answer cites them and ends with a person to contact.
- **Layer 2, my property:** an owner types their address. The tool finds the property's official City tax bills for 2026 and 2025 and shows the **total assessed value, the change from last year, any homestead exemption, and the tax bill total**, with links to the bill PDFs. The owner can then ask the chat about that property ("Did my assessment go up?"). It never shows owner names.

## What works
- **Layer 1 accuracy:** in a 10-question test the bot scored 6 fully correct and 4 mostly correct, with **no invented dates, dollar amounts, or rules**. It correctly says "I'm not sure" when a date isn't announced, refuses to value homes or predict appeals, stays inside Orleans Parish, and says it is a student prototype.
- **Layer 2 lookup:** address → City geocoder → City tax bill service (the same one behind nola.gov/find-tax-bill) → official bill PDFs. Tested on public buildings, the numbers match the bills exactly (e.g., 400 Poydras St: $5,532,520 assessed, −8.9% vs 2025, $814,442.28 tax). Fake and out-of-parish addresses are rejected with a clear message.
- **Handoffs:** questions about filing or winning an appeal get a refusal plus the right office and phone number (Assessor, City Council Board of Review, or Treasury).
- **Free to run:** Streamlit Community Cloud + Google Gemini free tier (`gemini-3.5-flash-lite`). The knowledge lives in CLAUDE.md, so updating that file updates the bot.

## What doesn't work yet
- **Citations are sometimes sloppy.** The bot occasionally cites a source that doesn't support a sentence, or cites a section number (e.g. "[2.8]") instead of a source.
- **Values lag a year.** The newest bill is tax year 2026. The 2027 values set in summer 2026 won't be on bills until about January 2027. We never received the Assessor's roll files, which would have the latest values.
- **Exempt properties** (government, churches, many nonprofits) have no tax bill, so lookups there return "no bill found."
- **Condos and shared parcels:** when several accounts share one point, the tool picks the one whose address matches. It doesn't handle unit numbers yet.
- **Not yet tested on a home with homestead or a freeze.** The parser reads the homestead line, but every test property so far was commercial.
- **Free-tier limits:** answers take about 10–25 seconds, and heavy use can hit Google's rate limit.

## Plan for the final
1. **Layer 3, market context:** compare an owner's change with their ZIP code using the Zillow data (all 17 Orleans ZIPs fell 5–27% since Jan 2023) and with nearby properties, and flag owners who may be paying on a frozen value above market (the freeze "tax trap").
2. **Fix citations:** add an automatic check that every cited number appears in the Sources list, and strip section-number citations.
3. **Use the Assessor roll files** (if provided) for current-year values, and add building permits since 2023 to explain value changes ("a renovation permit was issued here in 2024").
4. **Test with real homeowners' addresses** (with permission) to confirm homestead and freeze parsing, and add unit-number support for condos.
5. **Show the tax breakdown** from page 2 of the bill (how much goes to schools, police, the Sewerage & Water Board, and so on).
