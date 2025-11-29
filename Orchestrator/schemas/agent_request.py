from pydantic import BaseModel, Field

# pattern=r"^([a-zA-Z0-9?]{1,200})$",
class AgentRequest(BaseModel):
    Prompt: str = Field(None, description="Message sent to the chatbot by the user")
