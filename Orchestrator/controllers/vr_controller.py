from fastapi import APIRouter, BackgroundTasks, Depends
from schemas.vr_state_response import VRStateResponse
from schemas.vr_state_request import VRStateRequest
from services.agent_workflow import AgentWorkflow
from core.security import get_token_user_id
from fastapi.responses import StreamingResponse
from schemas.agent_request import AgentRequest
from config.config_vars import config
import logging

router = APIRouter(prefix=config.ENDPOINT_PREFIX)
logger = logging.getLogger(__name__)

@router.post("/state-info")
async def stream_info(request: AgentRequest, user_id: dict = Depends(get_token_user_id)):
    # We return information as streaming
    return StreamingResponse(AgentWorkflow().stream_vr_info(prompt=request.Prompt, user_id=user_id), media_type="text/event-stream")

@router.put("/state")
async def update_vr_states(request: AgentRequest, user_id: dict = Depends(get_token_user_id)):
    # Retrieves the modification structure from the Agent
    vr_state = await AgentWorkflow().get_vr_template(prompt=request.Prompt)
    return VRStateResponse.model_validate_json(vr_state)

@router.post("/state")
async def save_initial_state(vr_state: list[VRStateRequest], user_id: dict = Depends(get_token_user_id)):
    # Saves and sets up the vr state cache
    await AgentWorkflow().save_initial_vr_state()

@router.delete("/state")
async def delete_state(user_id: dict = Depends(get_token_user_id)):
    # The cache is cleared automatically upon the finalizing of the virtual reality simulation
    await AgentWorkflow().clear_user_cache()