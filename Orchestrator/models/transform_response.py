from pydantic import BaseModel, Field

class Component(BaseModel):
    Component: str | None = Field(None, pattern=r"^([a-zA-Z0-9?]{1,200})$", description="Specific component to be manipulated")
    State: str| None = Field(None, pattern=r"^([a-zA-Z0-9?]{1,200})$", description="New updated value for the component")

class TransformResponse(BaseModel):
    Tag: str | None = Field(None, pattern=r"^([a-zA-Z0-9?]{1,200})$", description="Search query to find the 3D elements")
    Components: list[Component] | None = Field(None, description="Every component that is part of the 3D element")

    def __init__(self, tag=None, components=None):
        super().__init__(Tag=self._get_tag_from_query(tag), Components=components)

    def _get_tag_from_query(self, query):
        return query.strip("@Tag:{}")