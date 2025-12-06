from redis.commands.search.query import Query
from config.redis_db import RedisClient
from config.config_vars import config
import logging
import json
import uuid
logger = logging.getLogger(__name__)

class VRRepository():
    def __init__(self):
        self.redis = RedisClient()

    async def save_all(self, content, user_id, namespace):
        for state in content:
            state["UserId"] = user_id
            id = f"{namespace}{str(uuid.uuid4())}"
            self.redis.client.json().set(id, "$", state)
        logger.info("%s units saved", len(content))
    
    def _find_ids(self, ids):
        modified_vr_objects = []
        for id in ids:
            modified_vr_objects.append(self.redis.client.json(id).get(id))
            logger.debug("Unit found: %s", self.redis.client.json(id).get(id))
        return modified_vr_objects
    
    async def update_all(self, content=None):
        logger.debug("Updating units: %s", content)
        search_results = self.search(query=content['tag'])

        for doc in search_results.docs:
            for doc_update in content["state"]:
                self.redis.client.json().set(doc.id, doc_update["prop"], doc_update["value"])

        logger.info("%s units updated", len(search_results.docs))
    
    def search(self, query):
        search_query = Query(config.REDIS_SEARCH_TEMPLATE.format(query, user_id)).paging(offset=0, num=config.REDIS_SEARCH_LIMIT)
        return self.redis.client.ft(config.VR_INDEX).search(search_query)
    
    def search_chat_history(self, query="agent_history"):
        search_results = self.search(query=query)
        chat_history = []
        keys_schema = ["Role", "Content"]
        for data in search_results.docs:
            chat_history.append({key.lower(): json.loads(data.json)[key] for key in keys_schema})
        return chat_history
    
    async def cache_real_time_state(self):
        # This realtime state summary contains less data and is more suitable to be passed to the agent as context

        # First the cached elements are deleted, and then recreated
        search_results = self.search("summarized_state")
        for vr in search_results.docs:
            self.redis.client.unlink(vr.id)

    
    def search_system_statistics(self):
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

    def get_real_time_summary(self):
        search_results = self.search("summarized_state")
        real_time_summary = []
        for doc in search_results.docs:
            real_time_summary.append(doc)

        logger.debug("Found %s summarized items", len(real_time_summary))
        return {"role": "assistant", 
                "content": f"The following is the summary of the current state of the 3D elements: {real_time_summary}"}
    
    async def purge_all(self, query="*"):
        logger.debug("Scanning for existing cache")
        cache = list(self.redis.client.scan_iter(query))
        if len(cache) < 1:
            logger.debug("No cache found")
            return
        for key in cache:
            self.redis.client.delete(key)
        logger.debug("Cache successfully deleted")