from redis.commands.search.query import Query
from config.redis_db import RedisClient
from config.config_vars import config
import logging
import uuid
logger = logging.getLogger(__name__)

class StateRepository():
    def __init__(self):
        self.redis = RedisClient()

    async def save(self, content, conversation_id):
        for state in content:
            state["ConversationId"] = conversation_id
            id = f"{config.VR_KEY_PREFIX}{str(uuid.uuid4())}"
            self.redis.client.json().set(id, "$", state)
        logger.info("%s units saved", len(content))
    
    async def update(self, content=None):
        logger.debug("Updating units: %s", content)
        search_results = self.search(query=content['tag'])

        for doc in search_results.docs:
            for doc_update in content["state"]:
                self.redis.client.json().set(doc.id, f"$.{doc_update["prop"]}", doc_update["value"])

        logger.info("%s units updated", len(search_results.docs))
    
    def search(self, query):
        search_query = Query(config.REDIS_SEARCH_TEMPLATE.format(query)).paging(offset=0, num=config.REDIS_SEARCH_LIMIT)
        return self.redis.client.ft(config.VR_INDEX).search(search_query)

    
    def search_state(self):
        # This real time state much data and is not passed as the agent context, but rather it is accessed in a function tool
        search_results = self.search()
        real_time_states = []
        for doc in search_results.docs:
            real_time_states.append(doc)

        logger.debug("Found %s detailed items", len(real_time_states))
        return {
            "role": "assistant", 
            "content": f"The following is the detailed 3D state of the elements for statistics: {real_time_states}"
                }


    async def delete(self, conversation_id="*"):
        logger.debug("Scanning for existing cache")
        cache = list(self.redis.client.scan_iter(conversation_id))
        if len(cache) < 1:
            logger.debug("No cache found")
            return
        for key in cache:
            self.redis.client.delete(key)
        logger.debug("Cache successfully deleted")