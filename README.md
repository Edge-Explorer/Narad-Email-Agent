# 🪄 Narad — Your AI-Powered Job Search Engine

> **Not just an email tool. A full AI-powered career management system that drafts, tracks, and manages your entire job search pipeline — all from your terminal.**

Narad is a command-line career agent powered by **Google Gemini 2.0 Flash**. It reads your CV, matches your skills to a Job Description, drafts a hyper-personalized email, tracks every application in a local CRM, and even preps you for interviews — all in one place.

---

## ✨ Features

| Feature | Command | Description |
|---|---|---|
| 🧠 **AI Email Drafting** | `send` | Gemini 2.0 Flash drafts tailored job emails. |
| 🎭 **Multi-CV Profiles** | `send` | Switch between different resume versions before each application. |
| 📄 **CV-Aware** | `send` | Narad reads your PDF resume and uses your real skills and links. |
| 🎯 **JD Matching** | `send` | Paste a Job Description — Narad matches your skills to it precisely. |
| 📎 **Auto Attachment** | `send` | Automatically attaches your selected resume PDF to the email. |
| 🔗 **Clickable Links** | `send` | LinkedIn, GitHub, and Portfolio are rendered as clickable HTML hyperlinks. |
| **Bold Formatting** | `send` | AI bold text (`**like this**`) is automatically converted to real HTML bold. |
| 📊 **Job Application CRM** | `stats` | Tracks every email you send (company, title, date, status) in a local database. |
| ⏰ **Smart Follow-ups** | `followup` | Identifies pending applications and drafts polite follow-up emails. |
| 🧠 **Interview Prep** | `interview` | Generates custom technical & behavioral questions based on your JD + CV. |
| 🔍 **Job Search Helper** | `search` | Helps you identify and target the right roles. |
| 📬 **Check Inbox** | `check` | Fetch and display your latest 5 emails. |
| 🧾 **AI Summarizer** | `summarize` | Get AI-generated summaries of your newest emails. |
| 🔐 **Secure by Design** | — | Uses Gmail App Passwords. Your credentials never leave your machine. |

---

## 🛠️ Tech Stack

- **AI Model**: Google Gemini 2.0 Flash (`google-generativeai`)
- **Email**: Gmail SMTP (Sending) + Gmail IMAP (Reading)
- **PDF Reading**: `pypdf`
- **Local CRM Database**: `SQLite` (built-in Python, no server needed)
- **Environment**: `python-dotenv`
- **Language**: Python 3.x

---

## ⚡ Quick Setup

### 1️⃣ Clone & Create Virtual Environment
```bash
git clone https://github.com/karanshelar8775/Narad-Email-Agent.git
cd Narad-Email-Agent
python -m venv venv

# Activate (Windows)
.\venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt
```

### 2️⃣ Configure Your `.env`
Copy the example file and fill in your credentials:
```bash
cp .env.example .env
```

Open `.env` and update:
```env
# ── Gmail Credentials ─────────────────────────────
EMAIL_ADDRESS="your_email@gmail.com"
EMAIL_PASSWORD="your_16_digit_app_password"
SMTP_SERVER="smtp.gmail.com"
SMTP_PORT=587
IMAP_SERVER="imap.gmail.com"

# ── Gemini API ─────────────────────────────────────
GEMINI_API_KEY="your_gemini_api_key_here"

# ── User Profile (For Personalized Drafting) ───────
USER_NAME="Your Full Name"
USER_UNIVERSITY="Your University"
USER_YEAR="Final Year"
USER_MAJOR="Your Major"
USER_PORTFOLIO="https://yourportfolio.vercel.app/"
```

> 💡 **Gmail App Password**: Go to [Google Account → Security → App Passwords](https://myaccount.google.com/security) and generate a 16-digit password.
>
> 💡 **Gemini API Key**: Get a free key from [Google AI Studio](https://aistudio.google.com/app/apikey).

### 3️⃣ Add Your Resume(s)
Drop your **CV/Resume PDF(s)** into the `resumes/` folder. Narad will auto-detect all of them. You can have multiple CVs for different roles!

---

## 🎮 How to Use

```bash
python main.py
```

You'll see the Narad command center:
```
============================================================
   🪄  NARAD | Your AI-Powered Job Search Engine
============================================================
Commands: 'send', 'check', 'summarize', 'stats', 'search', 'followup', 'interview', 'help', 'exit'
------------------------------------------------------------
```

---

### 📤 `send` — AI Job Application

1. Choose your **Career Profile** (which CV to use)
2. Describe your goal: `"Apply for Generative AI Developer at TCS"`
3. Enter **Recipient Name/Company** (optional but recommended)
4. Enter **Target Job Title** (e.g., `Generative AI Dev`)
5. **Paste the Job Description** — enter `DONE` when complete
6. Review the AI-drafted email
7. Confirm to send (your CV is auto-attached!) ✅

---

### 📊 `stats` — Application CRM

Every application you send is automatically logged. This command shows a summary:
```
Total Applications: 5
ID: 1 | Company: TCS | Status: Sent | Date: 2026-03-02
ID: 2 | Company: Idolize | Status: Sent | Date: 2026-03-02
```

---

### ⏰ `followup` — Smart Follow-up

Didn't hear back in 4 days? Narad will:
1. Check your CRM for pending applications.
2. Let you pick which one to follow up on.
3. Draft a polite, professional "Just checking in" email.

---

### 🧠 `interview` — Interview Prep

After sending your application, type `interview`:
1. Narad fetches the JD you applied to from the CRM.
2. It cross-references your CV skills against the JD.
3. Gemini generates:
   - **Top 5 Technical Questions**
   - **Top 3 Behavioral Questions**
   - **Your "Perfect Pitch"** (a personalized intro for this specific role)

---

### 📬 `check` — Inbox View

Fetches and displays your latest 5 emails:
```
[1] ✉️ FROM: hr@tcs.com | SUBJECT: Interview Invite | DATE: Mon, 02 Mar 2026
```

### 🧾 `summarize` — AI Email Summaries

Gemini reads your inbox and generates concise summaries for each email.

### 🔍 `search` — Job Hunt Mode

Helps you strategize your job search for a specific role.

---

## 📁 Project Structure

```
Narad-Email-Agent/
├── agents/
│   ├── base_agent.py         # Base class for all agents
│   └── email_agent.py        # SMTP + IMAP logic + HTML formatting + bold rendering
├── core/
│   ├── gemini_client.py      # Gemini 2.0 Flash API wrapper
│   ├── composer.py           # AI drafting engine (CV + JD + Portfolio aware)
│   ├── database.py           # SQLite CRM for tracking applications
│   ├── summarizer.py         # AI inbox summarization
│   └── reader.py             # Inbox fetching and formatting
├── resumes/                  # Drop your resume PDFs here (Multi-CV support!)
│   └── YourResume.pdf
├── utils/
│   └── helpers.py            # Shared utility functions
├── main.py                   # CLI entry point with all 7 commands
├── narad_crm.db              # Auto-created local CRM database (gitignored)
├── requirements.txt          # Python dependencies
├── .env.example              # Safe credentials template
├── .gitignore                # Keeps credentials and DB out of GitHub
└── README.md                 # This file
```

---

## 🔐 Security

- **`.env` is in `.gitignore`** — your credentials are **never pushed to GitHub**.
- **`narad_crm.db` is in `.gitignore`** — your job search data stays private.
- Uses **Gmail App Passwords**, not your main Google password.
- Your API key and email data stay **local to your machine**.

---

## 🚀 What Makes Narad Unique

Unlike generic email tools, Narad is a **full recruitment pipeline agent**:

1. It reads your **entire CV/Resume PDF** and your **Portfolio URL** on startup.
2. It reads the **JD you provide** and identifies key requirements.
3. Gemini **cross-references** your skills against the JD automatically.
4. The email is **100% unique** — tailored to that exact company and role.
5. The application is **logged** in your local CRM immediately.
6. After 4 days, **Narad follows up** so no opportunity slips through the cracks.
7. If you get an interview, Narad **prepares you** based on the same JD it applied to.

---

## 👨‍💻 Author

**Karan Rohidas Shelar** — Generative AI Developer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/karan-shelar-779381343)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/karanshelar8775)
[![Portfolio](https://img.shields.io/badge/Portfolio-FF5722?style=for-the-badge&logo=vercel&logoColor=white)](https://karan-portfolio-opal.vercel.app/)

---

*Built with ❤️ and Gemini 2.0 Flash — Because applying to jobs manually is so 2023.*
