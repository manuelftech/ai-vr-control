from datetime import datetime, timezone
from pydantic import BaseModel, Field

class AgentHistory(BaseModel):
    Tag: str | None = Field(None, description="Search query to find the message history of the agent")
    Role: str | None = Field(None, description="Role of the chat message (e.g., 'User', 'Assistant', 'System').")
    Content: str | None = Field(None, description="Previous prompts sent by the user.")

    def __init__(self, tag="agent_history", role="assistant", content=None):
        super().__init__(Tag=tag, Role=role, Content=content)