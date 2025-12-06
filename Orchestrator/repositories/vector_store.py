from openai import OpenAI
from config.config_vars import config

class VectorStore():

    def __init__(self):
        self.vector_stores = OpenAI().client.vector_stores

    def semantic_search(self, vector_store_id, search_query):
        results = self.vector_stores.search(
            vector_store_id=vector_store_id,
            query=search_query,
        )
        # Concatenate all the returned information to pass it to the new prompt
        context_info = ""
        for data in results.data:
            for content in data.content:
                context_info += f"{content.text}\n"
        return context_info
    
    def upload_pdf(self, filename):
        with open(filename, "rb") as file:
            self.vector_stores.file_batches.upload_and_poll(
                vector_store_id=config.VECTOR_STORE_KNOWLEDGE_BASE_ID,
                files=[file]
            )