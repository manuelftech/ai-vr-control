class InvalidAgentResponseError(Exception):
    """Custom exception for invalid client request made to the agent."""
    def __init__(self, message="Modification expected, informational request received."):
        super().__init__(message)