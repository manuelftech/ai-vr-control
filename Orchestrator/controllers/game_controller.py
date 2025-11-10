from fastapi import APIRouter, HTTPException, Request
#from service.init_chatbot import init_chatbot_v2
from fastapi.params import Depends
from pydantic import BaseModel
import logging
import json
import asyncio
import redis

logging.basicConfig(level=logging.DEBUG)
logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/game-objects")
#react_agent = init_chatbot_v2()

# class CoordinatesProperties():
#     X: float | None = None
#     Y: float | None = None
#     Z: float | None = None

# class TransformProperties():
#     Position: CoordinatesProperties | None = None
#     Rotation: CoordinatesProperties | None = None
#     Scale: CoordinatesProperties | None = None

# class ComponentProperties():
#     ConstantForce: CoordinatesProperties | None = None
#     Color: str | None = None

# class ObjectProperties():
#     Id: str
#     Tag: str | None = None
#     Component: ComponentProperties | None = None
#     Transform: TransformProperties | None = None

# class APIChatbotRequest():
#     Prompt: str
#     GameObjects: list[ObjectProperties] | None = None

@router.post("/status")
async def ask_question(request: Request):
    body = await request.json()
    logging.info("Prompt: %s", body["Prompt"])
    newId =  body["Prompt"]

    REDIS_HOST = 'localhost'
    REDIS_PASSWORD = "123456"
    REDIS_PORT = 6379
    INDEX_NAME = "GameObjectsIdx"
    KEY_PREFIX = "GameObjects:"

    client = redis.StrictRedis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        # ssl=USE_SSL,
        decode_responses=True 
    )

    """ Example prompt:
    Make the red cubes float. Query: "@Tag:{cube} @ComponentsColor:{red} @ComponentsConstantForce:[-inf 9.82]"

    Make the yellow cubes fall to the ground. Query: "@Tag:{cube} @ComponentsColor:{yellow} @ComponentsConstantForce:[+inf 9.82]"

    make the chairs have less gravity, and also make the green cubes fall to the ground. These are two queries:
    Query: "@Tag:{chair} @ComponentsConstantForce:[-inf 9.82]"
    Query: "@Tag:{cubes} @ComponentsColor:{green} @ComponentsConstantForce:[-inf 9.82]"
    """
    request = body["GameObjects"]

    client.json().set(f"GameObjects:array" , '$', request)

    #query = "@Tag:{cube} @ComponentsColor:{red} @ComponentsConstantForce:[-inf 9.82]"
    query = "@Tag:{cube}"
    search_results = client.ft(INDEX_NAME).search(query)
    search_results

    try:
        NEW_CONSTANT_FORCE_VALUE = 9.83
        updated_objects = []
        print(f"Found {search_results.total} objects to update.")
        for doc in search_results.docs:
            key = doc.id
            client.json().set(key, '$.Components.ConstantForce', NEW_CONSTANT_FORCE_VALUE)
            updated_json = client.json().get(key)
            updated_objects.append(updated_json)
            print(f"Updated key {key}, new force: {updated_json.get('constantforce')}")

        print("\n--- Summary of all updated objects (full JSON) ---")
        for obj in updated_objects:
            print(json.dumps(obj, indent=2))

    except redis.exceptions.ResponseError as e:
        print(f"\nAn error occurred, likely related to the index configuration or search query syntax:")
        print(e)
    except redis.exceptions.ConnectionError as e:
        print(f"\nCould not connect to Redis server. Ensure Redis Stack is running.")
        print(e)

    #result = react_agent.invoke(prompt_template)
    try:
        result = "test"
    except Exception as e:
        logging.error("Error processing response from chatbot: %s", e)
        raise e
    
    #await asyncio.sleep(10)
    
    return updated_objects