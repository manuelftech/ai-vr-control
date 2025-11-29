from pydantic import BaseModel, Field

class VRProperty(BaseModel):
    Name: str | None = Field(None, description="Specific component or transform element to be manipulated")
    State: str| None = Field(None, description="New updated value for the component")

class VRStateResponse(BaseModel):
    Tag: str | None = Field(None, description="Search query to find the 3D elements")
    Properties: list[VRProperty] | None = Field(None, description="Every component that is part of the 3D element")

    def __init__(self, tag=None, properties=None):
        if (properties):
            properties = self._format_properties(properties)
        if (tag):
            tag = self._format_tag(tag['search_query'])
        super().__init__(Tag=tag, Properties=properties)
    
    def _format_properties(self, transform_query):
        properties = []
        vr = VRProperty()
        for state in transform_query.properties_to_update:
            vr.Name = state["property"]
            vr.State = state["value"]
            properties.append(vr)

    def _format_tag(self, query):
        return query.strip("@Tag:{}")