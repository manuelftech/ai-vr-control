from fastapi import APIRouter, HTTPException, Request
from fastapi.params import Depends
from pydantic import BaseModel
from controllers.chatbot import ask_chatbot
import logging
import json
import asyncio
import redis

logging.basicConfig(level=logging.DEBUG)
logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/game-objects")

# curl -iX POST http://localhost:5000/game-objects/status -H 'Accept: application/json' -H 'Content-Type: application/json' -d '{"Prompt":"94f7cebe-f026-4645-b806-2540c9d97b85","GameObjects":[{"Id":"2fcc390c-82eb-443e-9859-68b260013c38","Tag":"cube","Name":"Cube_2","Components":{"ConstantForce":{"X":0.0,"Y":0.0,"Z":0.0},"Color":"RGBA(0.500, 0.500, 0.500, 1.000)"},"Transform":{"Position":{"X":1.72660947,"Y":0.02057181,"Z":1.23025346},"Rotation":{"X":-0.01323297,"Y":-0.01323998,"Z":0.706983149},"Scale":{"X":0.0401434377,"Y":0.435482621,"Z":0.03871146}}},{"Id":"09970fcd-af10-41b5-8155-9331b5257e6f","Tag":"cube","Name":"Cube_4","Components":{"ConstantForce":{"X":0.0,"Y":0.0,"Z":0.0},"Color":"RGBA(0.500, 0.500, 0.500, 1.000)"},"Transform":{"Position":{"X":1.72669375,"Y":0.02058626,"Z":1.096218},"Rotation":{"X":0.01223886,"Y":0.0164677016,"Z":0.7069632},"Scale":{"X":0.0401434377,"Y":0.435482621,"Z":0.03871146}}},{"Id":"d6aac6ea-d207-47af-aa4a-0b63c4d9e3f0","Tag":"cube","Name":"Cube_3","Components":{"ConstantForce":{"X":0.0,"Y":0.0,"Z":0.0},"Color":"RGBA(0.500, 0.500, 0.500, 1.000)"},"Transform":{"Position":{"X":1.72660708,"Y":0.0205765665,"Z":1.15137219},"Rotation":{"X":-0.0116377985,"Y":-0.014729972,"Z":0.7069903},"Scale":{"X":0.0401434377,"Y":0.435482621,"Z":0.03871146}}},{"Id":"94f7cebe-f026-4645-b806-2540c9d97b85","Tag":"cube","Name":"Cube_1","Components":{"ConstantForce":{"X":0.0,"Y":0.0,"Z":0.0},"Color":"RGBA(0.500, 0.500, 0.500, 1.000)"},"Transform":{"Position":{"X":1.745553,"Y":0.0205738526,"Z":1.33466673},"Rotation":{"X":0.00669958,"Y":0.00643909164,"Z":0.7070991},"Scale":{"X":0.0401434377,"Y":0.435482621,"Z":0.03871146}}}]}'

@router.post("/status")
async def ask_question(request: Request):
    body = await request.json()
    logging.info("Prompt: %s", body["Prompt"])
    game_objects = body["GameObjects"]

    REDIS_HOST = 'localhost'
    REDIS_PASSWORD = "123456"
    REDIS_PORT = 6379
    INDEX_NAME = "GameObjectsIdx"
    KEY_PREFIX = "GameObjects:"

    client = redis.StrictRedis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        decode_responses=True 
    )

    for game_object in game_objects:
        client.json().set(f"{KEY_PREFIX}{game_object['Id']}" , '$', game_object)

    template = ask_chatbot(str(body["Prompt"]))
    config = get_formatted_config(template)

    updated_gameobjects = []

    search_results = client.ft(INDEX_NAME).search(config.search_query)
    print(f"Found {search_results.total} objects to update.")
    for doc in search_results.docs:
        for update in config.properties_to_update:
            client.json().set(doc.id, update.property, update.value)
        print(f"[Validation] gameobject: {client.json().get(doc.id)}")
        updated_gameobjects.append(client.json().get(doc.id))
    
    return {"GameObjects": updated_gameobjects}

def get_formatted_config(template):
    print(f"[Validation] Received template: {template}")
    # 'Query:\n@Tag:{chair} \n@ComponentColor:{purple} \n@ComponentConstantForceY:[] \n\nProperties:\n$.Components.ConstantForce.Y = 9.83'
    query = ""
    properties = []
    
    from typing import Union
    
    class GameUpdateConfig:
        property: str
        value: Union[str | float]
    
    for line in template.split("\n"):
        if len(line) == 0:
            continue
        if "@" == line[0] and "[]" not in line and "{}" not in line:
            query = f"{query} {line}".strip()
        if "$" == line[0]:
            update = line.split("=")
            gameupdate_config = GameUpdateConfig()
            gameupdate_config.property = update[0].strip()
            gameupdate_config.value = update[1].strip()
            properties.append(gameupdate_config)
    
    class GameModificationConfig():
        search_query: str
        properties_to_update: list[GameUpdateConfig]
    
    conf = GameModificationConfig()
    conf.search_query = query
    conf.properties_to_update = properties
    print(f"[FORMATTING] Query: {conf.search_query}")
    for prop in conf.properties_to_update:
        print(f"[FORMATTING] Property: {prop}")
    return conf