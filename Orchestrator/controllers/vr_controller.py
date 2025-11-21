from repository.vr_repository import VRRepository
from services.chatgpt_service import ChatGPT
from fastapi import APIRouter, Request
import logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/virtual-reality-environment")

@router.post("/state")
async def ask_question(request: Request):
    request_body = await request.json()
    prompt = request_body["Prompt"]
    logging.debug("Prompt: %s", prompt)

    vr_repository = VRRepository()

    # Save virtual reality state to Redis
    vr_repository.saveAll(return_saved=False, vr_states=request_body["VirtualRealityState"])

    # Obtain the modification template for Redis from the Chatbot
    template_query = ChatGPT().ask(prompt)

    # Search and update the required VR elements in Redis
    updated_vr_state = vr_repository.updateAllWithTemplate(return_saved=True, template=template_query)
    
    return {"VirtualRealityState": updated_vr_state}