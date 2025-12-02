from pydantic import BaseModel, Field

class CoordinatesProperties(BaseModel):
    X: float = Field(None, description="X axis of the virtual reality object")
    Y: float = Field(None, description="Y axis of the virtual reality object")
    Z: float = Field(None, description="Z axis of the virtual reality object")

class ConstantForceProps(BaseModel):
    Force: CoordinatesProperties | None = Field(None, description="Force against gravity applied to the virtual reality object")
    RelativeTorque: CoordinatesProperties | None = Field(None, description="Rotation applied to the virtual reality object")

class ComponentsProperties(BaseModel):
    ConstantForce: ConstantForceProps | None = Field(None, description="Force applied to the virtual reality object")
    Color: str| None = Field(None, description="Color property of the Component", pattern=r"^(#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})|)$")
    Text: str | None = Field(None, description="Text property of the Component")

class TransformProperties(BaseModel):
    Position: CoordinatesProperties = Field(None, description="Position of the virtual reality object in the environment")
    Rotation: CoordinatesProperties = Field(None, description="Rotation of the virtual reality object in the environment")
    Scale: CoordinatesProperties = Field(None, description="Size of the virtual reality object in the environment")
    Reshape: float = Field(None, description="How much an element has changed its size.")

class VRStateRequest(BaseModel):
    Id: str = Field(None, description="Automatically generated Id for the duration of the scene session")
    Tag: str = Field(None, description="Tag of the object (e.g., television, cube, sofa)")
    Name: str = Field(None, description="Name of the object")
    Components: ComponentsProperties = Field(None, description="Components of the object (e.g., Renderer, ConstantForce)")
    Transform: TransformProperties = Field(None, description="Position of the object in the virtual reality environment")