# backend/core/narad_core.py

import sys
import os
import logging

# Add the parent directory of 'core' (i.e., the 'backend' folder) to the Python path.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.model_loader import load_model  # Make sure this file exists in backend/core/
from agents.github_agent import GitHubAgent  # GitHub Agent
from agents.email_agent import EmailAgent    # Email Agent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NaradCore")

def route_command(command: str, model) -> str:
    """Routes the user command to a specific agent based on a prefix."""
    lower_command = command.lower().strip()
    
    if lower_command.startswith("github:"):
        gh_command = command[len("github:"):].strip()
        agent = GitHubAgent()
        return agent.run(gh_command)
    elif lower_command.startswith("email:"):
        email_command = command[len("email:"):].strip()
        agent = EmailAgent()
        return agent.run(email_command)
    
    # If command doesn't target a specific agent, fallback to using the LLM model.
    return model.generate(command)

def main():
    """Entry point for the Narad core application."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    models_dir = os.path.join(base_dir, "models")
    model_file = "Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf"  # Update as needed.
    model_path = os.path.join(models_dir, model_file)
    
    try:
        model = load_model(model_path)
        logger.info("Narad Core: Model loaded successfully!")
    except Exception as e:
        logger.error("Error loading the model: %s", e)
        return

    logger.info("Narad is ready. Type your prompt or 'exit' to quit.")
    
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ["exit", "quit"]:
            logger.info("Exiting Narad. Goodbye!")
            break

        try:
            response = route_command(user_input, model)
            print("Narad:", response)
        except Exception as e:
            logger.error("Error generating response: %s", e)

if __name__ == "__main__":
    main()


