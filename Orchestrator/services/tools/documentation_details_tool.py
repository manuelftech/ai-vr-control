from agents import function_tool
from repositories.vector_store import VectorStore

@function_tool
def documentation_details_tool(technology: str):
    """
    Gets information about the documentation of the project itself, databases, programming languages and tools used to build this project.

    Args:
        technology: The technology of focus to search in the vector store.

    Returns:
        A list with text about the project details from e.g., "The LLM model used was gpt-5-nano".
    """

    context = VectorStore().semantic_search(technology)
    return context