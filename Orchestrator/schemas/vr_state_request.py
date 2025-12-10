from pydantic import BaseModel, Field

class CoordinatesProperties(BaseModel):
    x: float = Field(alias='X', description="X axis of the virtual reality object")
    y: float = Field(alias='Y', description="Y axis of the virtual reality object")
    z: float = Field(alias='Z', description="Z axis of the virtual reality object")

class ConstantForceProps(BaseModel):
    force: CoordinatesProperties | None = Field(alias='Force', description="Force against gravity applied to the virtual reality object")
    relative_torque: CoordinatesProperties | None = Field(alias='RelativeTorque', description="Rotation applied to the virtual reality object")

class ComponentsProperties(BaseModel):
    constant_force: ConstantForceProps | None = Field(alias='ConstantForce', description="Force applied to the virtual reality object")
    color: str| None = Field(alias='Color', description="Color property of the Component", pattern=r"^(#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})|)$")
    text: str | None = Field(alias='Text', description="Text property of the Component")

class TransformProperties(BaseModel):
    position: CoordinatesProperties = Field(alias='Position', description="Position of the virtual reality object in the environment")
    rotation: CoordinatesProperties = Field(alias='Rotation', description="Rotation of the virtual reality object in the environment")
    scale: CoordinatesProperties = Field(alias='Scale', description="Size of the virtual reality object in the environment")
    reshape: float = Field(alias='Reshape', description="How much an element has changed its size.")

class VRStateRequest(BaseModel):
    vr_id: str = Field(alias='VRId', description="Automatically generated Id for the duration of the scene session")
    tag: str = Field(alias='Tag', description="Tag of the object (e.g., television, cube, sofa)")
    name: str = Field(alias='Name', description="Name of the object")
    components: ComponentsProperties = Field(alias='Components', description="Components of the object (e.g., Renderer, ConstantForce)")
    transform: TransformProperties = Field(alias='Transform', description="Position of the object in the virtual reality environment")

class InitialVRStateProperties(BaseModel):
    vr_state: list[VRStateRequest]| None = Field(alias='VirtualRealityState', description="Complete scene elements")
