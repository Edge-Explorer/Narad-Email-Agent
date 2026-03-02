"""
base_agent.py — Base class for all agents.
"""

class BaseAgent:
    """Base class for all Narad agents."""
    def __init__(self, name: str):
        self.name = name

    def run(self, command: str) -> str:
        """Processes the given command. Must be overridden by subclasses."""
        raise NotImplementedError("Subclasses must implement the run() method.")
