from core.gemini_client import GeminiClient

class EmailSummarizer:
    """Uses Gemini to summarize inbox contents."""
    def __init__(self):
        self.gemini = GeminiClient()

    def summarize_emails(self, email_list: list) -> str:
        """Takes a list of email dicts and returns a summary of each."""
        if not email_list:
            return "No emails found to summarize."

        summary_results = []
        for e in email_list:
            # Build a simple summary prompt for each email content.
            prompt = f"""
            Summarize this email in ONE short bullet point:
            FROM: {e['from']}
            SUBJECT: {e['subject']}
            BODY: {e['body']}
            """
            summary = self.gemini.generate_content(prompt)
            summary_results.append(f"📧 From: {e['from']} | Subject: {e['subject']} -> {summary}")
        
        return "\n".join(summary_results)

    def generate_daily_digest(self, email_list: list) -> str:
        """Creates a high-level daily digest of all emails at once."""
        if not email_list:
              return "No emails found for today's summary."
              
        compiled_emails = "\n---\n".join([f"FROM: {e['from']} SUBJECT: {e['subject']} BODY: {e['body']}" for e in email_list])
        
        prompt = f"""
        Provide a concise 'Daily Digest' report for the following inbox contents:
        
        {compiled_emails}
        
        Group by urgency (High, Medium, Low) or by sender as appropriate.
        """
        return self.gemini.generate_content(prompt)

if __name__ == "__main__":
    # Test script for manual summarization.
    summarizer = EmailSummarizer()
    print("Testing Summarizer output...")
    # Add a test dictionary if needed.
