from fastapi import APIRouter, HTTPException, Request
from fastapi.params import Depends
import logging
logging.basicConfig(level=logging.DEBUG)
logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/game-objects")

@router.post("/status")
async def ask_question(request: Request):
    
    body_bytes = await request.body()
    body_string = body_bytes.decode('utf-8')
    logging.info("requests: %s", body_string)
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
        },
        {
            "Id": "def456",
            "Tag": "Chair",
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


""" 
void saveGameObjectStatus()
{
    status = getGameObjectsStatuses()
    status = [
        {
            instanceID: "ABC1234",
            coordinates: {
                x: 123,
                y: 123,
                z: 123
            }
            attributes: {
                assignedName: "cube"
                color: "red",
                gravity: "0.1"
            }
        },
        {
            instanceID: "JKL1234",
            coordinates: {
                x: 123,
                y: 123,
                z: 123
            }
            attributes: {
                assignedName: "chair",
                color: "red",
                gravity: "0.9"
            }
        },
    ]
    redis.saveInNewRecord(status);
}

void askChatbot(question)
{
    answer = chatbot.ask(question);
    newGameObjecstStatus = redis.getStatus();
    currentGameObjectStatus = newGameObjectStatus
    gameChatbotViualization.showNewMessage(answer)
}
 """