from fastapi import APIRouter, HTTPException, Request
from service.init_chatbot import init_chatbot_v2
from fastapi.params import Depends
from pydantic import BaseModel
import logging
import json
import asyncio

logging.basicConfig(level=logging.DEBUG)
logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/game-objects")
#react_agent = init_chatbot_v2()

@router.get("")
def validate(request):
    logging.info("Initializing promt building")
    logging.info(f"Request: {request}")
    
    prompt_template = {"input": f"""
        The following is a conversation between a Human and a Chatbot, the Chatbot summarizes the answer to no more than 30 words unless it is told by the Human to summarize it in a different amount of words, if the Chatbot does not know an answer it says that it does not now.
        Current conversation:

        \n\nHuman: {request}

        \n\nChatbot: 
        """}
    logging.info("Prompt: %s", prompt_template)
    try:
        #result = react_agent.invoke(prompt_template)
        result = None
    except Exception as e:
        logging.error("Error processing response from chatbot: %s", e)
        raise e
        
    logging.info("Answer: %s", result)
    return {'answer': result}

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

class APIChatbotRequest():
    Prompt: str
    GameObjects: list[ObjectProperties] | None = None

@router.post("/status")
async def ask_question(request: Request):
    body = await request.json()
    logging.info("Prompt: %s", body["Prompt"])
    newId =  body["Prompt"]
    try:
        result = "test"
    except Exception as e:
        logging.error("Error processing response from chatbot: %s", e)
        raise e
    
    await asyncio.sleep(10)
    
    return {"GameObjects": [
        {
            "Id": newId,
            "Tag": "cube",
            "Name": "Cube_2",
            "Components": {
                "ConstantForce": 9.82,
                "Color": "red"
            },
            "Transform": {
                "Position": {
                    "X": 1.98,
                    "Y": 1.287,
                    "Z": 1.331
                },
                "Rotation": {
                    "X": 0,
                    "Y": 0,
                    "Z": 5.17
                },
                "Scale": {
                    "X": 0.04014344,
                    "Y": 0.4354826,
                    "Z": 0.03871146
                },
            }
        }
    ]}
