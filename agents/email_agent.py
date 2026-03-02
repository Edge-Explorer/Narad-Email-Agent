import os
import smtplib
import imaplib
import email
import re
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

    def _format_body_to_html(self, text: str) -> str:
        """Helper to convert plain text into formatted HTML (links + bold)."""
        # Convert newlines to <br> first
        html = text.replace('\n', '<br>')

        # 1. Handle Markdown Bolding (**text**)
        bold_pattern = r'\*\*(.*?)\*\*'
        html = re.sub(bold_pattern, r'<b>\1</b>', html)

        # 2. Handle URLs (More robust regex)
        url_pattern = r'((?:https?://|www\.|[a-zA-Z0-9][-a-zA-Z0-9]*\.)[a-zA-Z0-9][-a-zA-Z0-9.]*\.(?:com|in|org|net|io|me|edu|app|dev|sh|ai|gov|mil|edu|[a-z]{2})(?:/[^\s<>"]*)?)'
        
        def replace_url_match(match):
            url = match.group(0)
            clean_url = url.rstrip('.,!?;:)')
            trailing_punct = url[len(clean_url):]
            href = clean_url if clean_url.startswith('http') else 'https://' + clean_url
            return f'<a href="{href}" style="color: #1a73e8; text-decoration: underline;">{clean_url}</a>{trailing_punct}'
        
        html = re.sub(url_pattern, replace_url_match, html)
        return html

    def send_email(self, to_address: str, subject: str, body: str, attachment_path: str = None) -> str:
        """Sends an email using SMTP with HTML formatting and optional attachment."""
        try:
            # Create a complex multi-part message (alternative for text/html, related for attachments)
            msg = MIMEMultipart("mixed")
            msg["From"] = f"Narad AI <{self.user_email}>"
            msg["To"] = to_address
            msg["Subject"] = subject
            
            # Create the alternative (body) part for plain text and HTML.
            alt_part = MIMEMultipart("alternative")
            msg.attach(alt_part)
            
            # Add plain text version.
            alt_part.attach(MIMEText(body, "plain"))
            
            # Create and add HTML version with clickable links.
            html_content = f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    {self._format_body_to_html(body)}
                    <br><br>
                    <hr style="border: none; border-top: 1px solid #eee;">
                    <p style="font-size: 12px; color: #888;">Sent via 🪄 Narad AI Email Agent</p>
                </body>
            </html>
            """
            alt_part.attach(MIMEText(html_content, "html"))
            
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
                
            return f"✅ Formatted Email (with clickable links) sent to {to_address}!"
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
