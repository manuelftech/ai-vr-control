from pydantic import BaseModel, Field

class ConversationStateResponse(BaseModel):
    ConversationId: str | None = Field(alias='conversation_id', description="Specific component or transform element to be manipulated")