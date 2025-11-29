from datetime import datetime, timezone
from pydantic import BaseModel, Field

class AgentHistory(BaseModel):
    Tag: str | None = Field(None, description="Search query to find the message history of the agent")
    Message: str | None = Field(None, description="Prompt sent to the agent")
    Date: datetime | None = Field(None, description="Date of the message")

    def __init__(self, tag="agent_history", date=None, message=None):
        if(not date):
            date = datetime.now(timezone.utc)
        super().__init__(Tag=tag, Date=date, Message=message)
    