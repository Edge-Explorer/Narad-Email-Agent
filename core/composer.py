from core.gemini_client import GeminiClient

class EmailComposer:
    """Uses Gemini to draft professional emails."""
    def __init__(self):
        self.gemini = GeminiClient()

    def draft_email(self, description: str, tone: str = "formal") -> dict:
        """
        Drafts an email based on a natural language prompt and a specified tone.
        :param description: What the email is about.
        :param tone: "formal" or "informal".
        """
        prompt = f"""
        Draft a {tone} email based on this description: '{description}'
        
        If formal: use professional language, proper greetings, and clear structure.
        If informal: use casual, friendly language and a relaxed tone.

        Provide the output in this EXACT format:
        SUBJECT: [Your Subject Line]
        BODY: [Your Email Body Content]
        """
        response = self.gemini.generate_content(prompt)
        
        # Parse the response strings into structured data.
        subject = ""
        body = ""
        
        if "SUBJECT:" in response and "BODY:" in response:
            try:
                subject_part = response.split("SUBJECT:")[1].split("BODY:")[0].strip()
                body_part = response.split("BODY:")[1].strip()
                return {"subject": subject_part, "body": body_part}
            except Exception:
                pass
        
        # Fallback if the model doesn't follow instructions perfectly.
        return {"subject": f"Narad {tone.capitalize()} Email", "body": response}

if __name__ == "__main__":
    # Test Drafting logic.
    composer = EmailComposer()
    draft = composer.draft_email("Follow up with my manager about the project deadline", tone="formal")
    print(f"Drafted (Formal) Subject: {draft['subject']}")
    print(f"Drafted Body:\n{draft['body']}")
