"""NOLA Assessment Navigator.

Layer 1 (general guidance): answers from CLAUDE.md sections 2, 4 and 5.
Layer 2 (my property): looks up an address in public City of New Orleans data
(property_lookup.py) and lets the owner ask questions about that record.

Hosted free on Streamlit Community Cloud, using Google Gemini's free tier.
"""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

import streamlit as st
from google import genai
from google.genai import errors, types

from property_lookup import LookupError as PropertyLookupError
from property_lookup import lookup, summary_for_model

DEFAULT_MODEL = "gemini-3.5-flash-lite"  # fast free-tier model; 3.8-flash timed out
MAX_QUESTIONS_PER_SESSION = 30  # stays well inside free-tier limits
MAX_QUESTION_CHARS = 1500
HISTORY_MESSAGES = 10  # past messages sent along with each new question

DISCLAIMER = (
    "This is a student prototype built for a class project. It is not an "
    "official government tool and may contain errors. Always confirm with the "
    "Orleans Parish Assessor's Office. Don't enter personal information."
)


# ---------- Knowledge base (read from CLAUDE.md) ----------

def extract_section(text: str, number: int) -> str:
    """Return the '## <number>. ...' section, up to the next '## ' heading."""
    match = re.search(rf"^## {number}\..*?(?=^## |\Z)", text, re.S | re.M)
    return match.group(0).strip() if match else ""


@st.cache_data
def load_knowledge() -> str:
    text = (Path(__file__).parent / "CLAUDE.md").read_text(encoding="utf-8")
    sections = [extract_section(text, n) for n in (2, 4, 5)]
    return "\n\n".join(s for s in sections if s)


def build_system_prompt(property_block: str | None) -> str:
    if property_block:
        prop_rules = f"""8. The user looked up a property. Its record is below in <property_record>, \
from the City's official tax bills; cite it as [P] and link the bill PDF. Use it to answer \
questions about "my property". Never show or guess the owner's name. Don't call the \
assessed value the market value; if asked, say residential property is assessed at 10% of \
market value [2], so a rough market value is about 10 times the assessed value, and that \
commercial buildings use 15%. Compare it with the rules in the notes, for example whether \
a homestead exemption appears on the bill.

<property_record>
{property_block}
</property_record>"""
    else:
        prop_rules = """8. No property has been looked up yet. If the user asks about their own \
property, tell them to use the "Look up a property" box at the top of the page."""

    return f"""You are the NOLA Assessment Navigator, a student-built assistant that \
helps New Orleans (Orleans Parish) property owners understand property assessments, \
exemptions, tax bills, and appeals.

Answer using ONLY the reference notes and property record below. Rules:
1. Cite sources only for facts that come from them. The notes number their sources \
(section 2.10). Put a number after a sentence only if that source says it. Don't cite \
sources for your own rules, for "I can't help with that," or for out-of-scope replies. \
End with a "**Sources:**" list containing every number you cited, each as a markdown \
link to that specific page.
2. If the notes don't answer the question, if a fact is marked [VERIFY], or if sources \
conflict, say so plainly ("I'm not sure about that") and point the user to the \
Assessor's Office. Never guess a deadline, dollar amount, or eligibility rule.
3. General information only. No legal or tax advice: don't tell someone whether they \
should appeal, what their property is worth, or whether they qualify. Say "you may \
qualify", never "you qualify" or "you likely qualify".
4. When a question is about a specific property, appeal, exemption, or bill, end by \
naming the right office to contact, with its phone number, from rule 4 in the notes.
5. Always say which year a deadline or rate applies to. Orleans Parish works one year \
ahead (section 2.0), so say both the year the rolls were open and the tax year. For \
future years, say the dates are expected, not announced.
6. Use plain language at about an 8th-grade reading level. Define terms the first \
time you use them. Keep answers short and use bullets for steps.
7. Orleans Parish only. If asked about another parish or an unrelated topic, say \
it's out of scope.
{prop_rules}
9. If asked what you are, say you are a student prototype, not an official tool.
10. Items marked TODO in the notes are unfinished project notes. Ignore them.
11. Today's date is {date.today():%B %d, %Y}. If the user mentions a date or a recent \
event (like "last month"), compare it with today and say which deadlines have already \
passed and which are still open.
12. When explaining how the tax is calculated, finish with the worked example's total \
from section 5.2 ($3,056.10 for a $300,000 East Bank home with homestead).
13. In answers about age or disability freezes, mention the freeze "tax trap" in 2.6.

<reference_notes>
{load_knowledge()}
</reference_notes>"""


# ---------- Gemini ----------

@st.cache_resource
def get_client() -> genai.Client:
    # 2-minute timeout and no silent retries, so problems show up as an
    # error message instead of an endless spinner.
    return genai.Client(
        api_key=st.secrets["GEMINI_API_KEY"].strip(),
        http_options=types.HttpOptions(
            timeout=120_000, retry_options=types.HttpRetryOptions(attempts=1)
        ),
    )


def to_gemini(messages: list[dict]) -> list[types.Content]:
    """Convert chat history to Gemini's format (it calls the assistant 'model')."""
    return [
        types.Content(
            role="user" if m["role"] == "user" else "model",
            parts=[types.Part(text=m["content"])],
        )
        for m in messages
    ]


def stream_answer(messages: list[dict], system_prompt: str):
    """Yield the answer piece by piece as Gemini writes it."""
    response = get_client().models.generate_content_stream(
        model=st.secrets.get("GEMINI_MODEL", DEFAULT_MODEL),
        contents=to_gemini(messages),
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )
    for chunk in response:
        if chunk.text:
            yield chunk.text


@st.cache_data(ttl=3600, show_spinner=False)
def cached_lookup(address: str) -> dict:
    return lookup(address)


def show_property(p: dict) -> None:
    newest = p["years"][0]
    older = p["years"][1] if len(p["years"]) > 1 else None
    st.markdown(f"**{p['site_address'] or p['matched_address']}** · tax bill no. `{p['tax_bill']}`")
    c1, c2, c3 = st.columns(3)
    delta = None
    if older and older["total_assessment"]:
        delta = f"{100 * (newest['total_assessment'] / older['total_assessment'] - 1):+.1f}% vs {older['year']}"
    c1.metric(f"Total assessed value ({newest['year']})", f"${newest['total_assessment']:,.0f}", delta, delta_color="off")
    c2.metric("Homestead exemption", f"${newest['homestead_exemption']:,.0f}",
              "on file" if newest["homestead_exemption"] else "none on bill", delta_color="off")
    c3.metric(f"{newest['year']} tax bill total",
              f"${newest['total_due']:,.2f}" if newest["total_due"] is not None else "n/a")
    st.caption(
        f"Land ${newest['land_assessment']:,.0f} + improvements ${newest['improvement_assessment']:,.0f}. "
        f"Assessed value is a share of market value (10% for homes). "
        f"Source: [{newest['year']} tax bill PDF]({newest['pdf_url']})"
        + (f" · [{older['year']} bill]({older['pdf_url']})" if older else "")
        + f" · [Pay / view on nola.gov]({p['pay_page']}). Owner names are not shown."
    )
    if not p["address_match"]:
        st.info("The bill lists a different address than the one you typed. Large parcels can hold several addresses; check the bill to be sure it's yours.")


# ---------- Page ----------

st.set_page_config(page_title="NOLA Assessment Navigator", page_icon="🏠")
st.title("🏠 NOLA Assessment Navigator")
st.caption("General guidance on Orleans Parish property assessments, exemptions, and appeals, plus a lookup for your own property.")
st.warning(DISCLAIMER)

with st.sidebar:
    st.header("About")
    st.write(
        "General answers come from public sources about Orleans Parish property "
        "assessment. Property lookups use the City of New Orleans' public tax bill "
        "records. Every answer lists its sources."
    )
    st.header("Talk to a person")
    st.markdown(
        "- [Orleans Parish Assessor's Office](https://nolaassessor.com) · (504) 754-8811\n"
        "- [City Council: assessments & appeals](https://council.nola.gov/resources/property-tax-assessments-and-appeals/) · (504) 658-1080\n"
        "- [Bureau of the Treasury (tax bills)](https://nola.gov/find-tax-bill/) · (504) 658-1701"
    )
    st.header("Try asking")
    st.markdown(
        "- How is my property tax calculated?\n"
        "- How do I apply for the homestead exemption?\n"
        "- What's the deadline to appeal my assessment?\n"
        "- After a lookup: Did my assessment go up? Do I have homestead?"
    )
    if st.button("Clear chat and property"):
        st.session_state.messages = []
        st.session_state.pop("property", None)
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---- Layer 2: property lookup ----
with st.expander("🔎 Look up a property", expanded="property" not in st.session_state):
    with st.form("lookup", clear_on_submit=False):
        addr = st.text_input("Street address in New Orleans", placeholder="e.g. 400 Poydras St")
        submitted = st.form_submit_button("Look up")
    if submitted and addr.strip():
        with st.spinner("Checking City of New Orleans records…"):
            try:
                st.session_state.property = cached_lookup(addr.strip()[:200])
            except PropertyLookupError as e:
                st.session_state.pop("property", None)
                st.error(str(e))
            except Exception as e:
                st.session_state.pop("property", None)
                st.error("The property lookup failed. Please try again in a minute.")
                st.caption(f"Details for the developer: {type(e).__name__}: {str(e)[:200]}")

if "property" in st.session_state:
    with st.container(border=True):
        show_property(st.session_state.property)
        st.caption("Ask the chat below about this property, e.g. \"Did my assessment go up?\"")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

question = st.chat_input("Ask about assessments, exemptions, appeals, or the property above…")

if question:
    asked = sum(1 for m in st.session_state.messages if m["role"] == "user")
    if asked >= MAX_QUESTIONS_PER_SESSION:
        st.info("You've reached the question limit for this session. Click 'Clear chat' to start over.")
        st.stop()

    question = question[:MAX_QUESTION_CHARS]
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    history = st.session_state.messages[-HISTORY_MESSAGES:]
    if history[0]["role"] != "user":  # history must start with a user message
        history = history[1:]

    prop = st.session_state.get("property")
    system_prompt = build_system_prompt(summary_for_model(prop) if prop else None)

    with st.chat_message("assistant"):
        answer = ""
        try:
            answer = st.write_stream(stream_answer(history, system_prompt))
            if not answer:
                answer = (
                    "Sorry, I couldn't answer that. Please contact the "
                    "[Assessor's Office](https://nolaassessor.com)."
                )
                st.markdown(answer)
        except errors.APIError as e:
            if e.code == 429:
                answer = "The chatbot is busy (free-tier limit reached). Please try again in a minute."
            elif e.code in (400, 401, 403):
                answer = "The chatbot isn't set up correctly. Check the API key and model name."
            else:
                answer = f"Something went wrong talking to the AI service (error {e.code}). Please try again."
            st.error(answer)
            st.caption(f"Details for the developer: {getattr(e, 'message', '') or str(e)[:300]}")
        except Exception as e:  # timeouts, network problems
            answer = "The AI service didn't respond. Please try again in a minute."
            st.error(answer)
            st.caption(f"Details for the developer: {type(e).__name__}: {str(e)[:300]}")

    st.session_state.messages.append({"role": "assistant", "content": answer})
