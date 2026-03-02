# 🪄 Narad Email Agent

> **An AI-powered CLI Email Assistant — built to send hyper-personalized, professional emails with zero effort.**

Narad is a command-line email agent powered by **Google Gemini 2.0 Flash**. It reads your CV, matches your skills to a Job Description, and drafts a perfectly tailored email — all from your terminal.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧠 **AI Drafting** | Gemini 2.0 Flash drafts emails based on your natural language description. |
| 🎭 **Formal & Informal Tone** | Choose between a professional or casual email tone. |
| 📄 **CV-Aware Personalization** | Narad reads your resume PDF and uses your real skills, links & projects. |
| 🎯 **JD Matching** | Paste a Job Description and Narad will tailor the email to match it precisely. |
| 📎 **Auto Attachment** | Automatically detects your resume PDF and offers to attach it. |
| 🔗 **Clickable Links** | LinkedIn, GitHub, and Portfolio links are rendered as clickable HTML hyperlinks. |
| 📬 **Check Inbox** | Fetch and display your latest 5 emails with sender, subject, and date. |
| 🧾 **AI Summarizer** | Get AI-generated summaries of your newest emails in seconds. |
| 🔐 **Secure by Design** | Uses Gmail App Passwords — your main password is never stored or used. |

---

## 🛠️ Tech Stack

- **AI Model**: Google Gemini 2.0 Flash (`google-generativeai`)
- **Email**: Gmail SMTP (Sending) + Gmail IMAP (Reading)
- **PDF Reading**: `pypdf`
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
```

> 💡 **Gmail App Password**: Go to [Google Account → Security → App Passwords](https://myaccount.google.com/security) and generate a 16-digit password.
> 
> 💡 **Gemini API Key**: Get a free key from [Google AI Studio](https://aistudio.google.com/app/apikey).

### 3️⃣ Add Your Resume
Drop your **CV/Resume PDF** into the root folder of the project. Narad will auto-detect it.

---

## 🎮 How to Use

```bash
python main.py
```

You'll see the main menu:
```
============================================================
   🪄  NARAD EMAIL AGENT | Powered by Gemini 2.0 Flash
============================================================
Commands: 'send', 'check', 'summarize', 'help', 'exit'
------------------------------------------------------------
```

### 📤 Sending a Job Application Email
1. Type **`send`**
2. Enter your goal: `Apply for Generative AI Developer role`
3. (Optional) Enter **Recipient Name/Company**: `Mr. Sharma at Idolize Business Solutions`
4. (Optional) **Paste a Job Description**:
   - Narad enters **[PASTE MODE]** with line numbers (`L1>`, `L2>`...)
   - Paste your entire JD, then type **`DONE`** on a new line and press Enter
5. Choose **`1`** for Formal or **`2`** for Informal tone
6. Review the AI-drafted email
7. When prompted, type **`y`** to attach your resume
8. Enter the **recipient's email address** and confirm to send ✅

### 📬 Checking Your Inbox
Type **`check`** — Narad fetches and displays your latest 5 emails:
```
[1] ✉️ FROM: hr@company.com | SUBJECT: Interview Scheduled | DATE: Mon, 02 Mar 2026
```

### 🧾 Summarizing Emails
Type **`summarize`** — Gemini AI reads your inbox and generates concise summaries.

### ❓ Help Menu
Type **`help`** — Shows all commands with detailed descriptions.

---

## 📁 Project Structure

```
Narad-Email-Agent/
├── agents/
│   ├── base_agent.py       # Base class for all agents
│   └── email_agent.py      # SMTP + IMAP email logic, HTML formatting
├── core/
│   ├── gemini_client.py    # Gemini 2.0 Flash API wrapper
│   ├── composer.py         # AI email drafting (CV + JD + Profile aware)
│   ├── summarizer.py       # AI email summarization
│   └── reader.py           # Inbox fetching and formatting
├── utils/
│   └── helpers.py          # Shared utility functions
├── main.py                 # CLI entry point
├── requirements.txt        # Python dependencies
├── .env.example            # Safe credential template
├── .gitignore              # Keeps credentials out of GitHub
└── README.md               # This file
```

---

## 🔐 Security

- **`.env` is in `.gitignore`** — your credentials are **never pushed to GitHub**.
- Uses **Gmail App Passwords**, not your main Google password.
- Your API key and email data stay **local to your machine**.

---

## 🚀 What Makes Narad Unique

Unlike generic email tools, Narad actually **understands who you are**:
1.  It reads your **entire CV/Resume PDF** on startup.
2.  It reads the **JD you provide** and identifies key requirements.
3.  Gemini 2.0 Flash **cross-references** your CV skills against the JD.
4.  The output is a **hyper-personalized email** that sounds like *you* wrote it.

---

## 👨‍💻 Author

**Karan Rohidas Shelar** — Generative AI Developer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/karan-shelar-779381343)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/karanshelar8775)

---

*Built with ❤️ and Gemini 2.0 Flash*
