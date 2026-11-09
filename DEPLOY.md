# How to put your chatbot online (free)

Total time: about 20 minutes. Cost: $0.

You'll use three free services:
- **Google AI Studio** gives you the AI (Gemini) and its API key.
- **GitHub** stores your code.
- **Streamlit Community Cloud** runs the code and gives you a public link.

---

## Step 1: Get a free Gemini API key (5 min)

1. Go to **https://aistudio.google.com** and sign in with a Google account.
2. Click **Get API key**, then **Create API key**.
3. Copy the key and keep it somewhere private, like a note on your computer.

> ⚠️ Treat this key like a password. Never paste it into GitHub, a screenshot, or your assignment.

> Note: on the free tier, Google may use what people type to improve its products. That's one reason the app tells users not to enter personal information.

---

## Step 2: Put the code on GitHub (5 min)

1. Go to **https://github.com** and sign up or sign in (free).
2. Click the **+** in the top right, then **New repository**.
   - Name: `nola-assessment-navigator`
   - Choose **Public**
   - Check **Add a README file**
   - Click **Create repository**
3. On the new repository page, click **Add file**, then **Upload files**.
4. Drag in these **3 files**:
   - `app.py`
   - `requirements.txt`
   - `CLAUDE.md`
5. Click **Commit changes**.

You don't need to upload `.streamlit/secrets.toml.example` or `.gitignore`. Your key goes into Streamlit in Step 3, never GitHub.

---

## Step 3: Launch it on Streamlit Community Cloud (5 min)

1. Go to **https://share.streamlit.io** and click **Continue with GitHub**. Allow access when asked.
2. Click **Create app**, then choose **Deploy a public app from GitHub**.
3. Fill in:
   - **Repository:** `your-username/nola-assessment-navigator`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL:** pick a name, like `nola-assessment-navigator`
4. Click **Advanced settings**. In the **Secrets** box, paste this, using your real key from Step 1:
   ```toml
   GEMINI_API_KEY = "paste-your-key-here"
   ```
5. Click **Save**, then **Deploy**.
6. Wait 1 to 3 minutes while it installs. Your chatbot then opens at a link like
   `https://nola-assessment-navigator.streamlit.app`.

**Copy that link into Section 6 of CLAUDE.md.** That's your "live link" for the assignment.

---

## Step 4: Test it and take screenshots (5 min)

Ask the 5 questions in the sidebar under **Try asking**. For each answer, check:
- Does it list **Sources** with links?
- Did it make up a deadline or number that isn't in CLAUDE.md?
- Did it say "I'm not sure" where it should?
- Did it point you to a person to contact?

Take a screenshot of each answer and note what it got wrong. That gives you Section 7 of the assignment.

---

## Updating the chatbot later

The chatbot reads its knowledge from `CLAUDE.md`. To change what it knows:
1. On GitHub, open `CLAUDE.md`, click the ✏️ pencil icon, make your edit, then **Commit changes**.
2. Streamlit picks up the change automatically within a minute or two. If it doesn't, open your app, click **Manage app** in the bottom right, then **Reboot app**.

For example, when you confirm a **[VERIFY]** fact, remove the tag and the chatbot will start stating it confidently.

---

## If something goes wrong

| What you see | Fix |
|---|---|
| "The chatbot isn't set up correctly" | The key is missing or mistyped. In Streamlit, go to your app, then **Settings**, then **Secrets**, and check the `GEMINI_API_KEY` line, including the quotes. |
| "Free-tier limit reached" | Too many questions too quickly. Wait a minute. |
| Error that mentions the model | Google may have renamed or retired the model. In **Secrets**, add a line `GEMINI_MODEL = "gemini-3.6-flash"`, or another free model listed at https://ai.google.dev/gemini-api/docs/models |
| `FileNotFoundError: CLAUDE.md` | You forgot to upload `CLAUDE.md` to GitHub. Upload it. |
| The app "fell asleep" | Free Streamlit apps sleep after a few days with no visitors. Click **Yes, get this app back up**. Open your link the day before it's graded. |
| Red error box with code | Click **Manage app** in the bottom right to see the log, then copy the error to Claude. |
