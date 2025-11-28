from config.redis_db import RedisClient
from config.config_vars import config
import logging
logger = logging.getLogger(__name__)

class VRRepository():
    def __init__(self):
        self.redis = RedisClient()

    async def saveAll(self, return_saved=False, vr_states=[]):
        modified_ids = []
        for vr_state in vr_states:
            id = f"{config.KEY_PREFIX}{vr_state.Id}"
            modified_ids.append(id)
            await self.save_single_object(id=id, property="$", vr_state=vr_state)
        if return_saved:
            return await self._find_ids(modified_ids=modified_ids)

    async def save_single_object(self, id=config.HISTORY_PREFIX, property="$", state=None):
        self.redis.client.json().set(id, property, state)
    
    async def _find_ids(self, ids):
        modified_vr_objects = []
        for id in ids:
            modified_vr_objects.append(self.redis.client.json(id).get(id))
            logging.debug("VR Status found: %s", self.redis.client.json(id).get(id))
        return modified_vr_objects
    
    async def updateAllWithTemplate(self, return_saved=False, template=None):
        logging.debug("Query: %s", template['search_query'])
        search_results = self.search(template['search_query'])

        modified_ids = []
        for doc in search_results.docs:
            for doc_update in template["properties_to_update"]:
                logging.debug("Updating Component: %s, State: %s", doc_update["property"], doc_update["value"])
                self.redis.client.json().set(doc.id, doc_update["property"], doc_update["value"])
                modified_ids.append(doc.id)

        if return_saved:
            return await self._find_ids(modified_ids)
        
    async def search(self, query=None):
        return self.redis.client.ft(config.INDEX_NAME).search(query)