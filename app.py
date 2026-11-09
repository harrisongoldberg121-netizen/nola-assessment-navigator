"""NOLA Assessment Navigator: Layer 1 chatbot (general guidance).

Hosted free on Streamlit Community Cloud, using Google Gemini's free tier.
The chatbot's knowledge comes from CLAUDE.md (sections 2, 4 and 5),
so when you update CLAUDE.md, the chatbot updates too.
"""

import re
from datetime import date
from pathlib import Path

import streamlit as st
from google import genai
from google.genai import errors, types

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


SYSTEM_PROMPT = f"""You are the NOLA Assessment Navigator, a student-built assistant that \
helps New Orleans (Orleans Parish) property owners understand property assessments, \
exemptions, tax bills, and appeals.

Answer using ONLY the reference notes below. Rules:
1. Cite a source for every fact. The notes number their sources (see section 2.10). \
Put the number after each fact, like [3], and end every answer with a "**Sources:**" \
list of the sources you used, each as a markdown link to that specific page.
2. If the notes don't answer the question, if a fact is marked [VERIFY], or if sources \
conflict, say so plainly ("I'm not sure about that") and point the user to the \
Assessor's Office. Never guess a deadline, dollar amount, or eligibility rule.
3. General information only. No legal or tax advice: don't tell someone whether they \
should appeal, what their property is worth, or how to file their taxes.
4. When a question is about a specific property, appeal, exemption, or bill, end by \
naming the right office to contact, with its phone number, from rule 4 in the notes.
5. Always say which year a deadline or rate applies to. Orleans Parish works one year \
ahead (section 2.0), so say both the year the rolls were open and the tax year. For \
future years, say the dates are expected, not announced.
6. Use plain language at about an 8th-grade reading level. Define terms the first \
time you use them. Keep answers short and use bullets for steps.
7. Orleans Parish only. If asked about another parish or an unrelated topic, say \
it's out of scope.
8. You can't look up individual properties yet. If asked, say so and point the user \
to the property search at nolaassessor.com.
9. If asked what you are, say you are a student prototype, not an official tool.
10. Items marked TODO in the notes are unfinished project notes. Ignore them.
11. Today's date is {date.today():%B %d, %Y}. If a deadline in the notes has already \
passed, say so and explain what the next opportunity is.

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


def stream_answer(messages: list[dict]):
    """Yield the answer piece by piece as Gemini writes it."""
    response = get_client().models.generate_content_stream(
        model=st.secrets.get("GEMINI_MODEL", DEFAULT_MODEL),
        contents=to_gemini(messages),
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
    )
    for chunk in response:
        if chunk.text:
            yield chunk.text


# ---------- Page ----------

st.set_page_config(page_title="NOLA Assessment Navigator", page_icon="🏠")
st.title("🏠 NOLA Assessment Navigator")
st.caption("General guidance on Orleans Parish property assessments, exemptions, and appeals.")
st.warning(DISCLAIMER)

with st.sidebar:
    st.header("About")
    st.write(
        "Answers come from a set of public sources about Orleans Parish "
        "property assessment. Every answer lists its sources."
    )
    st.header("Talk to a person")
    st.markdown(
        "- [Orleans Parish Assessor's Office](https://nolaassessor.com)\n"
        "- [City Council: assessments & appeals](https://council.nola.gov/resources/property-tax-assessments-and-appeals/)\n"
        "- [City of New Orleans Treasury](https://nola.gov/next/treasury/topics/how-taxes-are-calculated/)"
    )
    st.header("Try asking")
    st.markdown(
        "- How is my property tax calculated?\n"
        "- How do I apply for the homestead exemption?\n"
        "- What's the deadline to appeal my assessment?\n"
        "- What does the 2027 reassessment mean for me?\n"
        "- I'm 70. Can my assessment be frozen?"
    )
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

question = st.chat_input("Ask about assessments, exemptions, or appeals…")

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

    with st.chat_message("assistant"):
        answer = ""
        try:
            answer = st.write_stream(stream_answer(history))
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
