import os
import sys
from dotenv import load_dotenv

# Ensure we can import from our internal directories.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.email_agent import EmailAgent
from core.composer import EmailComposer
from core.summarizer import EmailSummarizer

load_dotenv()

class NaradCLI:
    """The central command hub for the Narad Email Agent."""
    def __init__(self):
        self.agent = EmailAgent()
        self.composer = EmailComposer()
        self.summarizer = EmailSummarizer()
        
    def show_header(self):
        """Displays the application branding."""
        print("=" * 60)
        print("   🪄  NARAD EMAIL AGENT | Powered by Gemini 2.0 Flash")
        print("=" * 60)
        print("Commands: 'send', 'check', 'summarize', 'help', 'exit'")
        print("-" * 60)

    def handle_send(self, user_command: str):
        """Handles the 'send' flow (asking for details, drafting, confirming)."""
        print("\n📝 Composition Mode: Speak naturally (e.g., 'Email my boss about the meeting results')")
        prompt = input("Compose description: ").strip()
        
        if not prompt:
            print("❌ Error: No description provided.")
            return

        print("\nChoose Tone:")
        print("[1] Formal (Professional & structured)")
        print("[2] Informal (Friendly & casual)")
        tone_choice = input("Choice (1 or 2, default 1): ").strip()

        tone = "informal" if tone_choice == "2" else "formal"

        print(f"\n✍️ Drafting {tone} email with Gemini...")
        draft = self.composer.draft_email(prompt, tone=tone)
        
        print(f"\n--- AI Drafted Content ({tone.capitalize()}) ---")
        print(f"Subject: {draft['subject']}")
        print(f"Body:\n{draft['body']}")
        print("-" * 25)
        
        recipient = input("Recipient email: ").strip()
        if not recipient:
            print("❌ Error: No recipient provided.")
            return
            
        confirm = input(f"Send to {recipient}? (y/n): ").strip().lower()
        if confirm == 'y':
            print("🚀 Sending...")
            result = self.agent.send_email(recipient, draft['subject'], draft['body'])
            print(result)
        else:
            print("🚫 Message discarded.")

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

    def run_loop(self):
        """Main application lifecycle."""
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
                elif cmd == 'help':
                    print("\n" + "=" * 60)
                    print("   📖  NARAD HELP MENU")
                    print("=" * 60)
                    print("- send      : Draft and send an email using AI (Formal/Informal).")
                    print("- check     : List your latest 5 emails (Sender, Subject, Date).")
                    print("- summarize : AI-generated summaries of your recent emails.")
                    print("- help      : Show this help menu.")
                    print("- exit      : Close the Narad Email Agent.")
                    print("=" * 60)
                elif not cmd:
                    continue
                else:
                    print(f"❓ Unknown command: {cmd}")
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    cli = NaradCLI()
    cli.run_loop()
