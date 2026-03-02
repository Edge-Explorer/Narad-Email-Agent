import os
from core.gemini_client import GeminiClient

class EmailComposer:
    """Uses Gemini to draft professional emails."""
    def __init__(self):
        self.gemini = GeminiClient()
        # Load user profile from environment variables.
        self.user_name = os.getenv("USER_NAME", "[Your Name]")
        self.user_university = os.getenv("USER_UNIVERSITY", "[Your University]")
        self.user_year = os.getenv("USER_YEAR", "[Your Year]")
        self.user_major = os.getenv("USER_MAJOR", "[Your Major]")

    def draft_email(self, description: str, tone: str = "formal") -> dict:
        """
        Drafts an email based on a natural language prompt and a specified tone.
        :param description: What the email is about.
        :param tone: "formal" or "informal".
        """
        # Create a user context string.
        user_context = f"My name is {self.user_name}. I am a {self.user_year} student at {self.user_university} majoring in {self.user_major}."
        
        prompt = f"""
        {user_context}
        
        Draft a {tone} email based on this description: '{description}'
        
        If formal: use professional language, proper greetings, and clear structure.
        If informal: use casual, friendly language and a relaxed tone.
        
        Auto-fill as much information as possible using my details. If you don't have enough details, use appropriate placeholders.

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
