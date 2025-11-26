from config.openai_agent import ChatGPT

class VectorStore():

    def __init__(self):
        self.vector_stores = ChatGPT().client.vector_stores

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