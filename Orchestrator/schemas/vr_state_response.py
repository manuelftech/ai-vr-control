from pydantic import BaseModel, Field
from typing import Optional, Union

class VRProperty(BaseModel):
    Name: str | None = Field(alias='prop', description="Specific component or transform element to be manipulated")
    State: Optional[Union[str, int, float]] = Field(alias='value', description="New updated value for the component")

class VRStateResponse(BaseModel):
    Tag: str | None = Field(alias='tag', description="Search query to find the 3D elements")
    Properties: list[VRProperty] | None = Field(alias='state', description="Every component that is part of the 3D element")