from pydantic import BaseModel, Field
from virtual_reality_request import ObjectsProperties

class VirtualRealityResponse(BaseModel):
    VirtualRealityState: ObjectsProperties = Field(None, description="List of elements with their virtual reality state")

    def __init__(self, virtual_reality_state=[]):
        self.virtual_reality_state = virtual_reality_state
