from services.agent_workflow_manager import Workflow
from schemas.vr_state_response import VRProperty, VRStateResponse
from schemas.vr_state_request import VRStateRequest
from repository.vr_repository import VRRepository
from fastapi import APIRouter, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from schemas.agent_request import AgentRequest
from models.agent_history import AgentHistory
from config.config_vars import config
import logging
import json
logger = logging.getLogger(__name__)
router = APIRouter(prefix=config.ENDPOINT_PREFIX)

@router.put("/state")
async def state(request: AgentRequest, background_tasks: BackgroundTasks):
    logging.debug("Prompt: %s", request.Prompt)
    # Retrieves the modification structure from the Agent
    vr_state = Workflow().start(prompt=request.Prompt)

    # The following processes execute without waiting for them to complete, but immediately returning the Controller response
    # Save chat history
    background_tasks.add_task(VRRepository().save_single_object, content=AgentHistory(message=request.Prompt))
    # Save updated Virtual Reality state
    background_tasks.add_task(VRRepository().updateAllWithTemplate, vr_state=vr_state)
    
    return VRStateResponse(vr_state)

@router.post("/state")
async def state(vr_state: list[VRStateRequest]):
    logging.debug("Received VR states: %s", vr_state)
    # Saves the initial Virtual Reality state to Redis
    await VRRepository().saveAll(vr_state=jsonable_encoder(vr_state))