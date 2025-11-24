from pydantic import BaseModel, Field
from models.virtual_reality_request import ObjectProperties

class VirtualRealityResponse(BaseModel):
    VirtualRealityState: list[ObjectProperties] | None = Field(None, description="List of elements with their virtual reality state")

    def __init__(self, virtual_reality_state=None, **kwargs):
        super().__init__(VirtualRealityState=virtual_reality_state, **kwargs)
