class EmailReader:
    """Handles fetching and basic processing of emails."""
    def __init__(self, agent):
        self.agent = agent

    def get_inbox_view(self, count: int = 5):
        """Fetches and formats recent emails."""
        return self.agent.fetch_latest_emails(count=count)
