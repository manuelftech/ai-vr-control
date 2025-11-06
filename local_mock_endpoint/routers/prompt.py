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
    
    return {'answer': "object successfully executed"}


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