from fastapi import APIRouter
from schemas.conversation_state_response import ConversationStateResponse
from schemas.vr_state_request import VRStateRequest
from services.agent_workflow import AgentWorkflow
from fastapi.responses import StreamingResponse
from schemas.agent_request import AgentRequest
from config.config_vars import config
import logging

router = APIRouter(prefix=config.ENDPOINT_PREFIX)
logger = logging.getLogger(__name__)

@router.post("/session-states")
async def stream_info(req: AgentRequest):
    # We return information as streaming
    return StreamingResponse(AgentWorkflow().stream_vr_info(prompt=req.Prompt, conversation_id=req.ConversationId), media_type="text/event-stream")

@router.put("/template")
async def update_vr_states(req: AgentRequest):
    # Retrieves the modification structure from the Agent
    return await AgentWorkflow().get_vr_template(prompt=req.Prompt, conversation_id=req.ConversationId)

@router.post("/session-states")
async def save_initial_state(vr_state: list[VRStateRequest]):
    # Saves and sets up the vr state cache
    conversation_id = AgentWorkflow().create_conversation()
    await AgentWorkflow().save_initial_vr_state(content=vr_state, conversation_id=conversation_id)
    return ConversationStateResponse(conversation_id=conversation_id)

@router.delete("/session-states")
async def delete_state(req: AgentRequest):
    # The cache is cleared automatically upon the finalizing of the virtual reality simulation
    await AgentWorkflow().clear_cache(conversation_id=req.ConversationId)