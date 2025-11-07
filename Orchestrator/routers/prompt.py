from fastapi import APIRouter, HTTPException, Request
from fastapi.params import Depends
import logging
import json
from pydantic import BaseModel
logging.basicConfig(level=logging.DEBUG)
logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/game-objects")

class CoordinatesProperties():
    X: float | None = None
    Y: float | None = None
    Z: float | None = None

class TransformProperties():
    Position: CoordinatesProperties | None = None
    Rotation: CoordinatesProperties | None = None
    Scale: CoordinatesProperties | None = None

class ComponentProperties():
    ConstantForce: CoordinatesProperties | None = None
    Color: str | None = None

class ObjectProperties():
    Id: str
    Tag: str | None = None
    Component: ComponentProperties | None = None
    Transform: TransformProperties | None = None

class APIChatbotRequest(BaseModel):
    Prompt: str
    GameObjects: list[ObjectProperties] | None = None
    class Config:
        arbitrary_types_allowed = True

@router.post("/status")
async def ask_question(request: APIChatbotRequest):
    logging.info("Prompt: %s", request.Prompt)
    try:
        result = "test"
    except Exception as e:
        logging.error("Error processing response from chatbot: %s", e)
        raise e
    
    return {"GameObjects": [
        {
            "Id": "abc123",
            "Tag": "cube",
            "Components": {
                "ConstantForce": 9.82,
                "Color": "red"
            },
            "Transform": {
                "Position": {
                    "x": 1.98,
                    "y": 1.287,
                    "z": 1.331
                },
                "Rotation": {
                    "x": 0,
                    "y": 0,
                    "z": 5.17
                },
                "Scale": {
                    "x": 0.04014344,
                    "y": 0.4354826,
                    "z": 0.03871146
                },
            }
        }
    ]}
