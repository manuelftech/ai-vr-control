import logging
import json
logging.basicConfig(level=logging.DEBUG)
logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def get_platform_instructions(input):
    logger.debug("[get_formatted_knowledge_base] Received template: %s", input["search_text"])
    # Do semantic search in database
    return input["search_text"]