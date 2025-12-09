from fastapi import APIRouter, BackgroundTasks
import structlog
from schemas.conversation_state_response import ConversationStateResponse
from schemas.vr_state_request import InitialVRStateProperties
from schemas.vr_state_response import VRStateResponse
from services.agent_workflow import AgentWorkflow
from fastapi.responses import StreamingResponse
from schemas.state_request import StateRequest
from schemas.cache_deletion_request import CacheDeletionRequest
from config.config_vars import config
logger = structlog.get_logger()
router = APIRouter(prefix=config.ENDPOINT_PREFIX)

@router.post("/session-states/stream")
async def stream_info(req: StateRequest):
    # We return information as streaming
    return StreamingResponse(AgentWorkflow().stream_vr_info(prompt=req.prompt, conversation_id=req.conversation_id), media_type="text/event-stream")

@router.put("/transform-template", response_model=VRStateResponse, response_model_by_alias=False)
async def update_vr_states(req: StateRequest, background_tasks: BackgroundTasks):
    # Retrieves the modification structure from the Agent
    transform_template = await AgentWorkflow().get_vr_template(prompt=req.prompt, conversation_id=req.conversation_id)
    # The updated Virtual Reality state is persisted
    background_tasks.add_task(AgentWorkflow().update_vr_state, states=transform_template, conversation_id=req.conversation_id)
    return transform_template

@router.post("/session-states", response_model=ConversationStateResponse, response_model_by_alias=False)
async def save_initial_state(req: InitialVRStateProperties):
    # Saves and sets up the vr state cache
    conv_ids = await AgentWorkflow().create_conversation()
    await AgentWorkflow().save_initial_vr_state(content=req.vr_state, conversation_id=conv_ids.conv_id_template)
    return conv_ids

@router.delete("/session-states")
async def delete_state(req: CacheDeletionRequest):
    # The cache is cleared automatically upon the finalizing of the virtual reality simulation
    await AgentWorkflow().clear_cache(conversatiod_ids=req.conversation_ids)