from pydantic import BaseModel, Field
from typing import Optional, Union

class VRProperty(BaseModel):
    Name: str | None = Field(None, description="Specific component or transform element to be manipulated")
    State: Optional[Union[str, int, float]] = Field(None, description="New updated value for the component")

class VRStateResponse(BaseModel):
    Tag: str | None = Field(None, description="Search query to find the 3D elements")
    Properties: list[VRProperty] | None = Field(None, description="Every component that is part of the 3D element")

    def __init__(self, vr_state=None):
        if (isinstance(vr_state, dict)):
            tag = self._format_tag(vr_state['search_query'])
            properties = self._format_properties(vr_state["properties_to_update"])
            super().__init__(Tag=tag, Properties=properties)
    
    def _format_properties(self, properties_to_update):
        properties = []
        for state in properties_to_update:
            vr = VRProperty()
            vr.Name = state["property"]
            vr.State = state["value"]
            properties.append(vr)
        return properties

    def _format_tag(self, query):
        return query.strip("@Tag:{}")