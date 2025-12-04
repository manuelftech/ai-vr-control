from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    Prompt: str = Field(None, pattern=r"^([a-zA-Z0-9\?\'\,\.\s\:]{1,200})$", description="Message sent to the chatbot by the user")
