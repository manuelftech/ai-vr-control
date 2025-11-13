from fastapi import APIRouter, HTTPException, Request
from fastapi.params import Depends
from pydantic import BaseModel
from services.chatbot_service import ask_chatbot
from repository.vr_repository import VRRepository
import logging
import json
import asyncio

logging.basicConfig(level=logging.DEBUG)
logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/virtual-reality-environment")

@router.post("/state")
async def ask_question(request: Request):
    request_body = await request.json()
    prompt = request_body["Prompt"]
    logging.info("Prompt: %s", prompt)

    vr_repository = VRRepository()

    # Save virtual reality state to Redis
    vr_repository.saveAll(return_saved=False, vr_states=request_body["VirtualRealityState"])

    # Obtain the modification template for Redis from the Chatbot
    template_query = ask_chatbot(prompt)

    template_query = get_formatted_config(template_query)

    # Search and update the required VR elements in Redis
    updated_vr_state = vr_repository.updateAllWithTemplate(return_saved=True, template=template_query)
    
    return {"VirtualRealityState": updated_vr_state}

def get_formatted_config(template):
    print(f"[Validation] Received template: {template}")
    query = ""
    properties = []
    
    from typing import Union
    
    class VRUpdateConfig:
        property: str
        value: Union[str | float]
    
    for line in template.split("\n"):
        if len(line.strip()) == 0:
            continue
        if "@" == line.strip()[0] and "[]" not in line and "{}" not in line:
            query = f"{query} {line}".strip()
        if "$" == line.strip()[0]:
            update = line.split("=")
            vrupdate_config = VRUpdateConfig()
            vrupdate_config.property = update[0].strip()
            try:
                vrupdate_config.value = float(update[1].strip())
            except:
                vrupdate_config.value = update[1].strip()
            properties.append(vrupdate_config)
    
    class VRModificationConfig():
        search_query: str
        properties_to_update: list[VRUpdateConfig]
    
    conf = VRModificationConfig()
    conf.search_query = query
    conf.properties_to_update = properties
    return conf