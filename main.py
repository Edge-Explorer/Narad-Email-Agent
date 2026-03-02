import os
import sys
from dotenv import load_dotenv

# Ensure we can import from our internal directories.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.email_agent import EmailAgent
from core.composer import EmailComposer
from core.summarizer import EmailSummarizer
from core.database import NaradDatabase

load_dotenv()

class NaradCLI:
    """The central command hub for the Narad Email Agent."""
    def __init__(self):
        self.agent = EmailAgent()
        self.summarizer = EmailSummarizer()
        self.db = NaradDatabase()
        # Initialize default composer (will switch profile in send)
        self.composer = EmailComposer()
        
    def show_header(self):
        """Displays the application branding."""
        print("=" * 60)
        print("   🪄  NARAD | Your AI-Powered Job Search Engine")
        print("=" * 60)
        print("Commands: 'send', 'check', 'summarize', 'stats', 'search', 'help', 'exit'")
        print("-" * 60)

    def _get_resume_path(self):
        """Finds any PDF in the root that looks like a resume."""
        files = os.listdir(".")
        pdf_files = [f for f in files if f.lower().endswith(".pdf") and ("resume" in f.lower() or "cv" in f.lower() or "karan" in f.lower())]
        return pdf_files[0] if pdf_files else None

    def handle_send(self, user_command: str):
        """Handles the 'send' flow with Multi-CV and CRM logging."""
        
        # 🎭 Multi-CV selection
        profiles = self.composer.list_profiles()
        print("\n📂 Available Career Profiles:")
        for idx, p in enumerate(profiles, 1):
            print(f"[{idx}] {p}")
        
        profile_choice = input("Select Profile (Number, default 1): ").strip()
        selected_cv = profiles[int(profile_choice)-1] if profile_choice.isdigit() and int(profile_choice) <= len(profiles) else profiles[0]
        
        # Switch composer to the selected profile
        self.composer = EmailComposer(cv_filename=selected_cv)
        print(f"✅ Active Profile: {selected_cv}")

        print("\n📝 Composition Mode: Speak naturally (e.g., 'Apply for the AI Developer role')")
        goal = input("Main goal/subject: ").strip()
        if not goal: return

        print("\n🎯 [Optional] Personalization:")
        recipient_info = input("Recipient Name/Company: ").strip()
        job_title = input("Target Job Title (e.g. Generative AI Dev): ").strip() or "Job Applicant"
        
        print("\n📥 [PASTE MODE] Paste Job Description below. When finished, type 'DONE'.")
        jd_lines = []
        while True:
            line = input("> ")
            if line.strip().upper() == "DONE": break
            jd_lines.append(line)
        job_description = "\n".join(jd_lines).strip()

        print(f"\n✍️ Drafting with {selected_cv}...")
        draft = self.composer.draft_email(goal, tone="formal", job_description=job_description, recipient_info=recipient_info)
        
        print(f"\n--- AI Draft Preview ---")
        print(f"Subject: {draft['subject']}\n")
        print(draft['body'])
        print("-" * 25)
        
        recipient_email = input("Recipient email: ").strip()
        if not recipient_email: return
            
        confirm = input(f"Send to {recipient_email}? (y/n): ").strip().lower()
        if confirm == 'y':
            resume_path = os.path.join("resumes", selected_cv)
            result = self.agent.send_email(recipient_email, draft['subject'], draft['body'], attachment_path=resume_path)
            print(result)
            
            # 💾 LOG TO DATABASE
            self.db.log_application(recipient_email, recipient_info, recipient_info, job_title, job_description)
            print("📈 Application logged to your CRM!")
        else:
            print("� Canceled.")

    def handle_stats(self):
        """Shows application statistics from the CRM."""
        print("\n📊 --- NARAD JOB CRM SUMMARY ---")
        apps = self.db.get_pending_followups()
        if not apps:
            print("📭 No applications logged yet!")
            return
            
        print(f"Total Applications: {len(apps)}")
        print("-" * 30)
        for a in apps[:5]: # Show latest 5
            print(f"ID: {a[0]} | Company: {a[3]} | Status: {a[5]} | Date: {a[6][:10]}")
        print("-" * 30)

    def handle_check(self):
        """Fetches and displays the most recent emails."""
        print("\n📬 Fetching latest emails...")
        emails = self.agent.fetch_latest_emails(count=5)
        
        if not emails:
            print("📭 Inbox is empty!")
            return
            
        for idx, e in enumerate(emails, 1):
            print(f"[{idx}] ✉️ FROM: {e['from']} | SUBJECT: {e['subject']} | DATE: {e['date']}")

    def handle_summarize(self):
        """Summarizes the inbox contents via Gemini."""
        print("\n🧠 AI Summarizing Inbox...")
        emails = self.agent.fetch_latest_emails(count=5)
        
        if not emails:
            print("📭 No emails found to summarize!")
            return
            
        summary = self.summarizer.summarize_emails(emails)
        print("\n--- Inbox Summary ---")
        print(summary)
        print("-" * 25)

    def handle_interview(self):
        """Generates interview prep questions based on the last application."""
        apps = self.db.get_pending_followups()
        if not apps:
            print("❌ No applications found in CRM to prepare for.")
            return
            
        last_app = apps[0] # The most recent one
        company = last_app[3]
        jd = last_app[8]
        
        print(f"\n🧠 Generating Interview Prep for {company}...")
        prompt = f"""
        I have an interview at {company}. 
        Here is the Job Description: {jd}
        Here is my CV context: {self.composer.cv_content[:2000]}
        
        Provide:
        1. Top 5 technical questions they might ask me.
        2. Top 3 behavioral questions.
        3. A "Perfect Pitch" for how I should introduce myself for this specific role.
        """
        response = self.composer.gemini.generate_content(prompt)
        print("\n--- 🔥 INTERVIEW PREP GUIDE ---")
        print(response)
        print("-" * 30)

    def handle_search(self):
        """Simple Job Search helper."""
        query = input("\n🔍 What kind of job are you looking for? (e.g. 'Remote Generative AI'): ").strip()
        print(f"Searching for '{query}' roles...")
        # In a real agent, we'd use a search API. For now, we guide the user to the best spots.
        print(f"\n💡 Narad Tip: I recommend checking LinkedIn and Wellfound for '{query}' roles.")
        print("Once you find a JD, come back here and use 'send' to apply!")

    def run_loop(self):
        """Main application lifecycle with all 6 advanced features."""
        self.show_header()
        
        while True:
            try:
                cmd = input("\nYou: ").strip().lower()
                
                if cmd in ['exit', 'quit']:
                    print("👋 Goodbye!")
                    break
                elif cmd == 'send':
                    self.handle_send(cmd)
                elif cmd == 'check':
                    self.handle_check()
                elif cmd == 'summarize':
                    self.handle_summarize()
                elif cmd == 'stats':
                    self.handle_stats()
                elif cmd == 'interview':
                    self.handle_interview()
                elif cmd == 'search':
                    self.handle_search()
                elif cmd == 'help':
                    print("\n" + "=" * 60)
                    print("   📖  NARAD HELP MENU")
                    print("=" * 60)
                    print("- send      : Draft & send application (Multi-CV + CRM logging).")
                    print("- check     : Fetch latest inbox emails.")
                    print("- summarize : AI summaries of your inbox.")
                    print("- stats     : View your Job Application CRM history.")
                    print("- search    : Help find new job opportunities.")
                    print("- interview : Get AI prep for your most recent application.")
                    print("- exit      : Close Narad.")
                    print("=" * 60)
                elif not cmd: continue
                else:
                    print(f"❓ Unknown command: {cmd}")
            except (KeyboardInterrupt, EOFError):
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    cli = NaradCLI()
    cli.run_loop()
