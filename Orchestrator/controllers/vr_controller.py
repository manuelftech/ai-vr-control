from fastapi import APIRouter, BackgroundTasks, Depends
from schemas.vr_state_response import VRStateResponse
from schemas.vr_state_request import VRStateRequest
from services.agent_workflow import AgentWorkflow
from repository.vr_repository import VRRepository
from core.security import get_token_user_id
from fastapi.responses import StreamingResponse
from schemas.agent_request import AgentRequest
from fastapi.encoders import jsonable_encoder
from config.config_vars import config
import logging

router = APIRouter(prefix=config.ENDPOINT_PREFIX)
logger = logging.getLogger(__name__)

@router.put("/state")
async def update_vr_states(request: AgentRequest, background_tasks: BackgroundTasks, user_id: dict = Depends(get_token_user_id)):
    # Retrieves the modification structure from the Agent
    vr_state = await AgentWorkflow().get_vr_template(prompt=request.Prompt)

    # Save updated Virtual Reality state
    background_tasks.add_task(VRRepository().update_all, content=vr_state, user_id=user_id)

    # Saves message history and Summarizes the previous history to make the agent episodic memory more concise
    background_tasks.add_task(AgentWorkflow().summarize_conversation_history(prompt=request.Prompt, user_id=user_id))
    return VRStateResponse.model_validate_json(vr_state)

@router.post("/state")
async def save_initial_state(vr_state: list[VRStateRequest], user_id: dict = Depends(get_token_user_id)):
    # The cache is cleared automatically before saving the new states
    await VRRepository().purge_all(user_id=user_id)

    # Saves the initial Virtual Reality state to Redis
    await VRRepository().save_all(content=jsonable_encoder(vr_state,user_id=user_id))

@router.delete("/state")
async def delete_state(user_id: dict = Depends(get_token_user_id)):
    # The cache is cleared automatically upon the finalizing of the virtual reality simulation
    await VRRepository().purge_all(user_id=user_id)

@router.post("/information")
async def stream_info(request: AgentRequest, user_id: dict = Depends(get_token_user_id)):
    # We return information as streaming
    return StreamingResponse(AgentWorkflow().stream_vr_info(prompt=request.Prompt, user_id=user_id), media_type="text/event-stream")