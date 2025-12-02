from services.agent_workflow_manager import Workflow
from schemas.vr_state_response import VRStateResponse
from schemas.vr_state_request import VRStateRequest
from repository.vr_repository import VRRepository
from fastapi import APIRouter, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from schemas.agent_request import AgentRequest
from models.agent_history import AgentHistory
from config.config_vars import config
import logging
logger = logging.getLogger(__name__)
router = APIRouter(prefix=config.ENDPOINT_PREFIX)

@router.put("/state")
async def state(request: AgentRequest, background_tasks: BackgroundTasks):
    logging.debug("Prompt: %s", request.Prompt)
    # Retrieves the modification structure from the Agent
    vr_state = Workflow().start(prompt=request.Prompt)

    # The following processes execute without waiting for them to complete, but immediately returning the Controller response
    # Save chat history
    background_tasks.add_task(VRRepository().save_all, content=AgentHistory(message=request.Prompt).create_completed_response())
    # Save updated Virtual Reality state
    background_tasks.add_task(VRRepository().update_all, content=vr_state)
    # Save temporal real-time data for next request
    background_tasks.add_task(VRRepository().cache_real_time_state)
    
    response = VRStateResponse(vr_state=vr_state)
    logging.debug("Modification properties Response: %s", response)
    return response

@router.post("/state")
async def state(vr_state: list[VRStateRequest], background_tasks: BackgroundTasks):
    # The cache is cleared automatically before saving the new states
    await VRRepository().purge_all()

    logging.debug("Received VR states: %s", vr_state)
    # Saves the initial Virtual Reality state to Redis
    await VRRepository().save_all(content=jsonable_encoder(vr_state))

    # Save temporal real-time data for next request
    background_tasks.add_task(VRRepository().cache_real_time_state)
    logging.info("Successfully generated environment cache")

@router.delete("/state")
async def state():
    # The cache is cleared automatically upon the finalizing of the virtual reality simulation
    await VRRepository().purge_all()
    logging.info("Successfully deleted environment cache")