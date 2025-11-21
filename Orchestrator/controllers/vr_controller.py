from repository.vr_repository import VRRepository
from services.chat_workflow_manager import Workflow
from fastapi import APIRouter, Request
from config import config
import logging
logger = logging.getLogger(__name__)
router = APIRouter(prefix=config.ENDPOINT_PREFIX)

@router.post("/state")
async def state(request: Request):
    request_body = await request.json()
    prompt = request_body["Prompt"]
    logging.debug("Prompt: %s", prompt)

    # Get the repository to interact with the Redis Database
    vr_repository = VRRepository()

    # Save virtual reality state to Redis
    vr_repository.saveAll(return_saved=False, vr_states=request_body["VirtualRealityState"])

    # Retrieves the modification template for Redis from the Chatbot
    template_query = Workflow.start(prompt)

    # Search and update the required VR elements in Redis
    updated_vr_state = vr_repository.updateAllWithTemplate(return_saved=True, template=template_query)
    
    return {"VirtualRealityState": updated_vr_state}