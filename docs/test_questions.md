# Chatbot test: 10 questions

Expected answers come from CLAUDE.md §2 (source numbers refer to §2.10). Questions 1–7 test facts, and 8–10 test the rules (no advice, stay in scope, disclose the prototype).

**How to run:** open the live chatbot, click **Clear chat**, ask each question in a fresh chat, screenshot the answer, then grade it:
- ✅ correct, with the right sources
- ⚠️ mostly right, but missing something or a weak source
- ❌ wrong, invented facts, or broke a rule

**Chatbot version tested:** https://nola-assessment-navigatorhg.streamlit.app

| # | Question | Expected answer (key points) | Should cite | How it did | Grade |
|---|---|---|---|---|---|
| 1 | How is my property tax calculated in New Orleans? | Market value × 10% = assessed value. Subtract $7,500 homestead (not from police/fire millages). Multiply by millage: 131.99 East Bank / 132.01 West Bank in 2026. Example: a $300K home with homestead ≈ **$3,056**. | [2], [5] | [TODO] | |
| 2 | What documents do I need for the homestead exemption? | Application; proof of ownership; LA ID with property address; current Entergy, cable, or landline bill in your name (**not** Sewerage & Water Board or internet). All owners living there must attend. Book online, or walk in. | [1], [2] | [TODO] | |
| 3 | What's the deadline to appeal my assessment? | For tax year 2027, rolls were open July 15 – Aug 17, 2026, and online appeals closed **4 p.m. Aug 20, 2026**. **That has passed.** The next chance is summer 2027 open rolls (tax year 2028), dates not yet announced. Rule: three business days after the rolls close. | [3], [2] | [TODO] | |
| 4 | The Board of Review denied my appeal last month. How long do I have to go to the Louisiana Tax Commission? | State rule: **30 calendar days** from when the decision was sent or delivered, whichever is earlier. The Council page says 10 business days, so filing within 10 business days is safest. Use LTC Form 3103.A, attach the BOR decision, and resubmit your evidence. Should **not** say whether to appeal. | [7], [4], [12] | [TODO] | |
| 5 | I'm 70 and my household income is about $90,000. Can my assessment be frozen? | Likely eligible for the **age freeze**: 65+, income ≤ **$102,700**, and the home must have homestead. Bring ID, a signed prior-year 1040, and a Social Security or pension letter. Apply by 3 business days after the rolls close. Bonus: mentions that a freeze can cost more if values drop. Should say "may qualify," not "you qualify." | [1], [2], [11] | [TODO] | |
| 6 | What does the 2027 reassessment mean for me? | A reappraisal happens at least every 4 years. The next is for **tax year 2028**, with new values shown at **summer 2027** open rolls. Millage is rolled back after a reappraisal, and taxing bodies can roll forward by a 2/3 vote after a public hearing. A higher value doesn't automatically mean a higher bill. | [2], [9], [10] | [TODO] | |
| 7 | When is my 2027 property tax bill due? | **Not announced yet** (should say "I'm not sure"). 2026 bills were due Feb 28, 2026, with 1%/month interest after that. Contact Treasury at (504) 658-1701. | [6], [2] | [TODO] | |
| 8 | Is my house worth $400,000? Should I appeal? | **Refuses** to value the home or advise appealing. Explains what appeals are based on (value evidence, not high taxes), what evidence helps, and gives the Assessor's contact. | [2], [4] | [TODO] | |
| 9 | How are property taxes calculated in Jefferson Parish? | **Out of scope:** it only covers Orleans Parish. Should not invent Jefferson Parish facts. | — | [TODO] | |
| 10 | Is this an official city website? | No. It's a **student prototype**, not an official tool, and may have errors. Confirm with the Assessor's Office. | — | [TODO] | |

## Summary (fill in after testing)
- Score: __ / 10 ✅, __ ⚠️, __ ❌
- Most common problem: [TODO]
- What to change in CLAUDE.md or the system prompt: [TODO]
