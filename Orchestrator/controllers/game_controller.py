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

# curl -iX POST http://localhost:5000/game-objects/status -H 'Accept: application/json' -H 'Content-Type: application/json' -d '{"Prompt":"94f7cebe-f026-4645-b806-2540c9d97b85","GameObjects":[{"Id":"2fcc390c-82eb-443e-9859-68b260013c38","Tag":"cube","Name":"Cube_2","Components":{"ConstantForce":{"X":0.0,"Y":0.0,"Z":0.0},"Color":"RGBA(0.500, 0.500, 0.500, 1.000)"},"Transform":{"Position":{"X":1.72660947,"Y":0.02057181,"Z":1.23025346},"Rotation":{"X":-0.01323297,"Y":-0.01323998,"Z":0.706983149},"Scale":{"X":0.0401434377,"Y":0.435482621,"Z":0.03871146}}},{"Id":"09970fcd-af10-41b5-8155-9331b5257e6f","Tag":"cube","Name":"Cube_4","Components":{"ConstantForce":{"X":0.0,"Y":0.0,"Z":0.0},"Color":"RGBA(0.500, 0.500, 0.500, 1.000)"},"Transform":{"Position":{"X":1.72669375,"Y":0.02058626,"Z":1.096218},"Rotation":{"X":0.01223886,"Y":0.0164677016,"Z":0.7069632},"Scale":{"X":0.0401434377,"Y":0.435482621,"Z":0.03871146}}},{"Id":"d6aac6ea-d207-47af-aa4a-0b63c4d9e3f0","Tag":"cube","Name":"Cube_3","Components":{"ConstantForce":{"X":0.0,"Y":0.0,"Z":0.0},"Color":"RGBA(0.500, 0.500, 0.500, 1.000)"},"Transform":{"Position":{"X":1.72660708,"Y":0.0205765665,"Z":1.15137219},"Rotation":{"X":-0.0116377985,"Y":-0.014729972,"Z":0.7069903},"Scale":{"X":0.0401434377,"Y":0.435482621,"Z":0.03871146}}},{"Id":"94f7cebe-f026-4645-b806-2540c9d97b85","Tag":"cube","Name":"Cube_1","Components":{"ConstantForce":{"X":0.0,"Y":0.0,"Z":0.0},"Color":"RGBA(0.500, 0.500, 0.500, 1.000)"},"Transform":{"Position":{"X":1.745553,"Y":0.0205738526,"Z":1.33466673},"Rotation":{"X":0.00669958,"Y":0.00643909164,"Z":0.7070991},"Scale":{"X":0.0401434377,"Y":0.435482621,"Z":0.03871146}}}]}'



@router.post("/status")
async def ask_question(request: Request):
    body = await request.json()
    logging.info("Prompt: %s", body["Prompt"])
    prompt =  body["Prompt"]
    game_objects = body["GameObjects"]
    print(f"Prompt: {prompt}")
    print(f"GameObjects: {game_objects}")

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

    print("[START] Loop")
    for index, game_object in enumerate(game_objects):
        print(f"{index}: {game_object}")
        client.json().set(f"{KEY_PREFIX}{game_object['Id']}" , '$', game_object)
    print("[END] loop")

    #query = "@Tag:{cube} @ComponentsColor:{red} @ComponentsConstantForce:[-inf 9.82]"
    query = "@Tag:{cube}"
    search_results = client.ft(INDEX_NAME).search(query)
    search_results
    print(f"Search results: {search_results}")
    updated_objects = []

    try:
        NEW_CONSTANT_FORCE_VALUE = 9.83
        NEW_CONSTANT_COLOR_VALUE = "red"
        updated_objects = []
        print(f"Found {search_results.total} objects to update.")
        for doc in search_results.docs:
            key = doc.id
            client.json().set(key, '$.Components.ConstantForce', NEW_CONSTANT_FORCE_VALUE)
            client.json().set(key, '$.Components.Color', NEW_CONSTANT_COLOR_VALUE)
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
    
    # #await asyncio.sleep(10)
    
    return {"GameObjects": updated_objects}