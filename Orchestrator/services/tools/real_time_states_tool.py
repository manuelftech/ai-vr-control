from repositories.vr_states_repository import StateRepository
from agents import function_tool

@function_tool
def real_time_states_tool(tag: str, conversation_id: str):
    """
    Gets information about the 3D virtual state element's states, including quantity, levitation, rotation and color.

    Args:
        tag: The tag to be used to search for types of elemnts, e.g, "sofa", "cube", "rack".
        conversation_id: The current conversation_id of the OpenAI Agent conversation, to search by this context only.

    Returns:
        A list with json with each element details, including their color, reshape, levitation, and other properties.
    """

    state_details = StateRepository().search(tag=tag, conversation_id=conversation_id)
    return state_details