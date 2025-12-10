from openai import OpenAI
from config.config_vars import config
import structlog
logger = structlog.get_logger()

class VectorStore():
    def __init__(self):
        self.vector_stores = OpenAI().vector_stores

    def semantic_search(self, search_query):
        logger.debug("Searching in Vector Store. Query: %s", search_query)
        results = self.vector_stores.search(
            vector_store_id=config.VECTOR_STORE_KNOWLEDGE_BASE_ID,
            query=search_query,
        )

        # We return the complete set of data
        context_info = []
        for data in results.data:
            for content in data.content:
                context_info.append(content.text)
        logger.debug("Vector Store found %s items", len(context_info))
        return context_info
    
    def upload_pdf(self, filename):
        with open(filename, "rb") as file:
            self.vector_stores.file_batches.upload_and_poll(
                vector_store_id=config.VECTOR_STORE_KNOWLEDGE_BASE_ID,
                files=[file]
            )