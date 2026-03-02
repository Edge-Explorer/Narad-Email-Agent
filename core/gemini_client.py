import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class GeminiClient:
    """Handles communications with the Gemini 2.0 Flash API."""
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY NOT FOUND in .env file!")
        
        # Configure the Google AI SDK with the provided API key.
        genai.configure(api_key=self.api_key)
        
        # Use the gemini-2.0-flash model for fast, low-latency responses.
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    def generate_content(self, prompt: str) -> str:
        """Sends a prompt to Gemini 2.0 Flash and returns the generated text."""
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Error communicating with Gemini: {e}"

# Simple test if run directly
if __name__ == "__main__":
    client = GeminiClient()
    print("Testing Gemini 2.0 Flash connection...")
    print("Gemini Response:", client.generate_content("Say hello from Gemini 2.0 Flash!"))
