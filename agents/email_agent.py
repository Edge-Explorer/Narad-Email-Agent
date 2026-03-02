import os
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from agents.base_agent import BaseAgent
from dotenv import load_dotenv

load_dotenv()

class EmailAgent(BaseAgent):
    """
    Narad Email Agent:
    Uses SMTP for sending and IMAP for reading emails from Gmail.
    """
    def __init__(self):
        super().__init__("Email Agent")
        
        # Pull login credentials from environment variables.
        self.user_email = os.getenv("EMAIL_ADDRESS")
        self.password = os.getenv("EMAIL_PASSWORD")
        
        # Server addresses and ports.
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.imap_server = os.getenv("IMAP_SERVER", "imap.gmail.com")

    def send_email(self, to_address: str, subject: str, body: str, attachment_path: str = None) -> str:
        """Sends an email using SMTP, with optional attachment."""
        try:
            # Prepare the email headers and body.
            msg = MIMEMultipart()
            msg["From"] = self.user_email
            msg["To"] = to_address
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))
            
            # Add attachment if provided.
            if attachment_path and os.path.exists(attachment_path):
                try:
                    filename = os.path.basename(attachment_path)
                    with open(attachment_path, "rb") as attachment:
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition", f"attachment; filename= {filename}")
                    msg.attach(part)
                except Exception as attach_err:
                    print(f"⚠️ Warning: Could not attach file: {attach_err}")

            # Use smtplib to connect to the server and send the message.
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Upgrade connection to secure TLS.
                server.login(self.user_email, self.password)
                server.sendmail(self.user_email, to_address, msg.as_string())
                
            return f"✅ Email successfully sent to {to_address}!"
        except Exception as e:
            return f"❌ Error sending email: {e}"

    def fetch_latest_emails(self, count: int = 5) -> list:
        """Fetches the latest N emails from the inbox via IMAP."""
        emails_found = []
        try:
            # Connect to IMAP server and login.
            mail = imaplib.IMAP4_SSL(self.imap_server)
            mail.login(self.user_email, self.password)
            mail.select("inbox")  # Select the inbox folder.

            # Search for ALL emails but pick the last 'count' IDs.
            status, messages = mail.search(None, "ALL")
            if status != "OK":
                return []
            
            msg_ids = messages[0].split()
            latest_ids = msg_ids[-count:]  # Keep the most recent ones.
            latest_ids.reverse()  # Latest first.

            for msg_id in latest_ids:
                # Fetch each individual email.
                status, msg_data = mail.fetch(msg_id, "(RFC822)")
                if status != "OK":
                    continue
                
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        raw_msg = email.message_from_bytes(response_part[1])
                        subject = raw_msg["subject"]
                        sender = raw_msg["from"]
                        date = raw_msg["date"]
                        
                        # Extract the body content from the email.
                        body = ""
                        if raw_msg.is_multipart():
                            for part in raw_msg.walk():
                                if part.get_content_type() == "text/plain":
                                    body += part.get_payload(decode=True).decode("utf-8", "ignore")
                        else:
                            body = raw_msg.get_payload(decode=True).decode("utf-8", "ignore")
                        
                        emails_found.append({
                            "id": msg_id.decode(),
                            "from": sender,
                            "subject": subject,
                            "date": date,
                            "body": body[:500]  # Limit body content for efficiency.
                        })
            
            mail.logout()
            return emails_found
        except Exception as e:
            print(f"Error fetching emails: {e}")
            return []

    def run(self, command: str) -> str:
        """Entry point for commands directed to the email agent."""
        # This will be expanded as we integrate more features.
        return f"Email Agent received: {command}"

if __name__ == "__main__":
    # Test script for manually sending/fetching.
    agent = EmailAgent()
    print("Testing fetch...")
    recent = agent.fetch_latest_emails(count=2)
    for e in recent:
        print(f"--- From: {e['from']} | Subject: {e['subject']} ---")
