import os
import pypdf
from core.gemini_client import GeminiClient

class EmailComposer:
    """Uses Gemini to draft professional emails."""
    def __init__(self):
        self.gemini = GeminiClient()
        # Load user profile from environment variables.
        self.user_name = os.getenv("USER_NAME", "[Your Name]")
        self.user_university = os.getenv("USER_UNIVERSITY", "[Your Year] Student at [Your University]")
        self.user_major = os.getenv("USER_MAJOR", "[Your Major]")
        
        # Load CV content if available.
        self.cv_content = self._load_cv_content()

    def _load_cv_content(self) -> str:
        """Finds and reads the text from the CV/Resume PDF in the root directory."""
        try:
            # Look for any PDF file that might be a resume in the root.
            root_files = os.listdir(".")
            pdf_files = [f for f in root_files if f.lower().endswith(".pdf") and ("resume" in f.lower() or "cv" in f.lower() or "karan" in f.lower())]
            
            if not pdf_files:
                return ""
            
            cv_path = pdf_files[0] # Use the first match.
            reader = pypdf.PdfReader(cv_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            print(f"⚠️ Warning: Could not read CV content: {e}")
            return ""

    def draft_email(self, description: str, tone: str = "formal") -> dict:
        """
        Drafts an email based on a natural language prompt and a specified tone.
        :param description: What the email is about.
        :param tone: "formal" or "informal".
        """
        # Create a user context string.
        user_context = f"My name is {self.user_name}. Educational background: {self.user_university}, Major: {self.user_major}."
        if self.cv_content:
            user_context += f"\n\nHere is the content of my CV/Resume for more details:\n{self.cv_content[:3000]}" # Limit to 3000 chars.
        
        prompt = f"""
        User Context:
        {user_context}
        
        Draft a {tone} email based on this description: '{description}'
        
        If formal: use professional language, proper greetings, and clear structure.
        If informal: use casual, friendly language and a relaxed tone.
        
        Auto-fill as much information as possible using the provided CV details (links, skills, projects).
        If you don't have enough details, use appropriate placeholders.

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
