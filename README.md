# 🪄 Narad Email Agent

An AI-powered Email Assistant built with Python and **Gemini 2.0 Flash**. Narad helps you manage your inbox and draft emails using natural language—all through a clean CLI.

---

## 🚀 Key Features

- **🧠 AI Email Drafting**: Speak naturally (e.g., *"Email my boss about the meeting"*) and let Gemini write the subject and body.
- **🌗 Tone Control**: Choose between **Formal** (Professional/Structured) and **Informal** (Friendly/Casual) for every draft.
- **📬 Inbox Reader**: Quickly list your latest emails directly from your terminal using IMAP.
- **📚 AI Summarizer**: Get a bulleted summary of your recent emails to save time.
- **⚡ Fast & Secure**: Powered by the ultra-fast Gemini 2.0 Flash API and supports Gmail App Passwords.

---

## 🛠️ Setup & Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/karanshelar8775/Narad-Email-Agent.git
cd Narad-Email-Agent
```

### 2️⃣ Create Virtual Environment & Install Dependencies
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 3️⃣ Configure Environment Variables
Copy `.env.example` to `.env` and fill in your details:
- **`EMAIL_ADDRESS`**: Your Gmail address.
- **`EMAIL_PASSWORD`**: Your [Gmail App Password](https://myaccount.google.com/security) (16 digits).
- **`GEMINI_API_KEY`**: Your key from [Google AI Studio](https://aistudio.google.com/app/apikey).

---

## 🎮 How to Use

Run the agent:
```bash
python main.py
```

### 📖 Available Commands
- **`send`**: Draft and send an email using AI (pick Formal/Informal tone).
- **`check`**: List your latest 5 emails (Sender, Subject, Date).
- **`summarize`**: Get AI-generated summaries of your inbox.
- **`help`**: Show the detailed help menu.
- **`exit`**: Close the agent.

---

## 🔐 Security & Privacy
- **`.gitignore`** is configured to protect your `.env` and `venv` from being pushed to GitHub.
- **App Passwords** ensure your main Google password remains safe.

---

## 🛠️ Built With
- **Python** (SMTP/IMAP)
- **Gemini 2.0 Flash API**
- **dotenv** (Secure config)
