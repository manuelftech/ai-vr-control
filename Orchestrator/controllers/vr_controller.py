from models.transform_response import TransformResponse
from models.virtual_reality_request import ObjectProperties
from services.agent_workflow_manager import Workflow
from repository.vr_repository import VRRepository
from fastapi import APIRouter, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from models.agent_request import AgentRequest
from config.config_vars import config
import logging
logger = logging.getLogger(__name__)
router = APIRouter(prefix=config.ENDPOINT_PREFIX)

@router.put("/state")
async def state(request: AgentRequest, background_tasks: BackgroundTasks):
    logging.debug("Prompt: %s", request.Prompt)
    # Retrieves the modification structure from the Agent
    transform_query = Workflow().start(prompt=request.Prompt)
    # Returns the HTTP response without waiting for the function "save_single_object" to complete
    background_tasks.add_task(VRRepository().save_single_object, state=request.Prompt)
    background_tasks.add_task(VRRepository().updateAllWithTemplate, template=transform_query)
    return TransformResponse(tag=transform_query.search_query, components=transform_query.properties_to_update)

@router.post("/state")
async def state(vr_state: list[ObjectProperties]):
    # Saves the initial virtual reality state to Redis
    VRRepository().saveAll(vr_states=jsonable_encoder(vr_state))