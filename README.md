# 🪄 Narad — Your AI-Powered Job Search Engine

> **Not just an email tool. A full AI-powered career management system that drafts, tracks, and manages your entire job search pipeline — available as a CLI or as a plug-and-play MCP Server inside your AI Assistant.**

Narad is powered by **Google Gemini 2.0 Flash**. It reads your CV, matches your skills to a Job Description, drafts a hyper-personalized email, tracks every application in a local CRM, preps you for interviews, and can now be used **directly from inside Antigravity, Cursor, or Claude Desktop** — without ever opening a terminal.

---

## ✨ Features

| Feature | Command/Tool | Description |
|---|---|---|
| 🧠 **AI Email Drafting** | `send` / `apply_for_job` | Gemini 2.0 Flash drafts tailored job emails. |
| 🎭 **Multi-CV Profiles** | `send` | Switch between different resume versions before each application. |
| 📄 **CV-Aware** | auto | Narad reads your PDF resume and uses your real skills and links. |
| 🎯 **JD Matching** | `send` | Paste a Job Description — Narad matches your skills to it precisely. |
| 📎 **Auto Attachment** | auto | Automatically attaches your selected resume PDF to the email. |
| 🔗 **Clickable Links** | auto | LinkedIn, GitHub, and Portfolio are rendered as clickable HTML hyperlinks. |
| **Bold Formatting** | auto | AI bold text is automatically converted to real HTML bold. |
| 📊 **Job Application CRM** | `stats` / `get_job_stats` | Tracks every email you send in a local SQLite database. |
| ⏰ **Smart Follow-ups** | `followup` | Identifies pending applications and drafts polite follow-up emails. |
| 🧠 **Interview Prep** | `interview` / `prepare_for_interview` | Generates custom questions based on your JD + CV. |
| 🔍 **Job Search Helper** | `search` | Helps you identify and target the right roles. |
| 📬 **Check Inbox** | `check` / `check_inbox` | Fetch and display your latest 5 emails. |
| 🧾 **AI Summarizer** | `summarize` / `summarize_inbox` | Get AI-generated summaries of your newest emails. |
| 🔌 **MCP Server** | Plug-and-play | Narad works directly inside Antigravity, Cursor, or Claude Desktop. |

---

## 🛠️ Tech Stack

- **AI Model**: Google Gemini 2.0 Flash (`google-generativeai`)
- **Email**: Gmail SMTP (Sending) + Gmail IMAP (Reading)
- **PDF Reading**: `pypdf`
- **Local CRM Database**: `SQLite` (built-in Python, no server needed)
- **MCP Protocol**: `fastmcp` (Model Context Protocol)
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
```bash
cp .env.example .env
```

Open `.env` and fill in:
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

> 💡 **Gmail App Password**: [Google Account → Security → App Passwords](https://myaccount.google.com/security)
>
> 💡 **Gemini API Key**: [Google AI Studio](https://aistudio.google.com/app/apikey)

### 3️⃣ Add Your Resume(s)
Drop your **CV/Resume PDF(s)** into the `resumes/` folder. Narad will auto-detect all of them.

---

## 🎮 Mode 1: CLI Usage (Classic)

```bash
python main.py
```

```
============================================================
   🪄  NARAD | Your AI-Powered Job Search Engine
============================================================
Commands: 'send', 'check', 'summarize', 'stats', 'search', 'followup', 'interview', 'help', 'exit'
```

| Command | What it does |
|---|---|
| `send` | Pick your CV → Paste JD → AI drafts → Sends + logs to CRM |
| `stats` | View your Job Application CRM history |
| `followup` | Draft follow-up emails for pending applications |
| `interview` | Get AI interview prep for your most recent application |
| `check` | See your latest emails |
| `summarize` | AI summaries of your inbox |
| `search` | Get job hunt tips |

---

## 🔌 Mode 2: MCP Server (AI Assistant Integration)

This is the **Power User** mode. Narad can be connected to **Antigravity, Cursor, or Claude Desktop** and used directly from your AI chat — no terminal needed.

### ✅ Step 1: Verify `mcp_config.json` exists
The file should be at:
```
C:\Users\<YourName>\.gemini\antigravity\mcp_config.json
```

With this content:
```json
{
    "mcpServers": {
        "narad": {
            "command": "C:\\Users\\<YourName>\\Desktop\\Narad-Email-Agent\\venv\\Scripts\\python.exe",
            "args": [
                "C:\\Users\\<YourName>\\Desktop\\Narad-Email-Agent\\mcp_server.py"
            ],
            "env": {
                "PYTHONPATH": "C:\\Users\\<YourName>\\Desktop\\Narad-Email-Agent"
            }
        }
    }
}
```
> ⚠️ Replace `<YourName>` with your actual Windows username.

### ✅ Step 2: Enable in Your AI Assistant

**For Antigravity (VSCode):**
1. Open Settings → Customizations
2. Find "INSTALLED MCP SERVERS"
3. Click **Refresh** 🔄 (close and reopen if needed)
4. `narad` should appear with a **blue toggle** ✅

**For Cursor:**
1. Open Cursor Settings → Features → MCP
2. Click "Add New MCP Server"
3. Name: `narad`, Command: the python path above

**For Claude Desktop:**
Add the same block to `claude_desktop_config.json` in your Claude app data folder.

### ✅ Step 3: Use it with Natural Language!

Once connected, your AI Assistant can access all of Narad's tools. Just talk naturally:

| What you say | What Narad does |
|---|---|
| *"Check my inbox for any recruiters"* | Calls `check_inbox` → returns your emails |
| *"Apply for the AI role at TCS"* | Calls `apply_for_job` → drafts + sends + logs |
| *"Summarize my emails"* | Calls `summarize_inbox` → AI summary |
| *"How many jobs have I applied to?"* | Calls `get_job_stats` → shows CRM data |
| *"Prep me for my TCS interview"* | Calls `prepare_for_interview` → custom guide |

---

## 🧰 MCP Tools Exposed

| Tool | Description |
|---|---|
| `apply_for_job` | Drafts and sends a personalized job application email with CV attached |
| `check_inbox` | Returns the latest N emails from your Gmail inbox |
| `summarize_inbox` | Returns an AI-generated summary of your recent emails |
| `get_job_stats` | Returns application stats from the local CRM database |
| `prepare_for_interview` | Generates custom interview prep guide from the JD + CV |
| `list_cv_profiles` (Resource) | Lists all available resume PDFs in the `resumes/` folder |

---

## 📁 Project Structure

```
Narad-Email-Agent/
├── agents/
│   ├── base_agent.py         # Base class for all agents
│   └── email_agent.py        # SMTP + IMAP + HTML formatter + bold rendering
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
├── main.py                   # CLI entry point (Mode 1)
├── mcp_server.py             # MCP Server entry point (Mode 2) ← NEW
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
- All processing happens **locally on your machine**.

---

## 👨‍💻 Author

**Karan Rohidas Shelar** — Generative AI Developer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/karan-shelar-779381343)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/karanshelar8775)
[![Portfolio](https://img.shields.io/badge/Portfolio-FF5722?style=for-the-badge&logo=vercel&logoColor=white)](https://karan-portfolio-opal.vercel.app/)

---

*Built with ❤️ and Gemini 2.0 Flash — Because applying to jobs manually is so 2023.*
