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

    async def saveAll(self, return_saved=False, vr_state=[]):
        modified_ids = []
        for state in vr_state:
            id = f"{config.VR_KEY_PREFIX}{state['Id']}"
            modified_ids.append(id)
            await self.save_single_object(id=id, property="$", content=state)
        logger.info("VR states successfully saved in Redis")
        if return_saved:
            return await self._find_ids(modified_ids=modified_ids)

    async def save_single_object(self, id=None, property="$", content=None):
        id = self._validate_id(id)
        content = self._validate_content(content)
        self.redis.client.json().set(id, property, content)
    
    async def _find_ids(self, ids):
        modified_vr_objects = []
        for id in ids:
            modified_vr_objects.append(self.redis.client.json(id).get(id))
            logging.debug("VR Status found: %s", self.redis.client.json(id).get(id))
        return modified_vr_objects
    
    async def updateAllWithTemplate(self, return_saved=False, vr_state=None):
        logging.debug("Updating Component: %s", json.loads(vr_state))
        search_results = self.search(query=vr_state['search_query'])

        modified_ids = []
        for doc in search_results.docs:
            for doc_update in vr_state["properties_to_update"]:
                self.redis.client.json().set(doc.id, doc_update["property"], doc_update["value"])
                modified_ids.append(doc.id)

        logging.info("%s Components updated", len(modified_ids))
        if return_saved:
            return await self._find_ids(modified_ids)
    
    def search(self, query=None):
        search_query = Query(query).paging(offset=0, num=config.REDIS_SEARCH_LIMIT)
        return self.redis.client.ft(config.VR_INDEX).search(search_query)
    
    def search_chat_history(self, query="@Tag:{agent_history}"):
        logging.debug("Query: %s", query)
        search_results = self.search(query=query)
        chat_history = ""
        for data in search_results.docs:
            chat_history += f"User: {json.loads(data.json)['Message']}\n"
        return chat_history
    
    def search_vr_summary(self, query="-@Tag:{agent_history}"):
        logging.debug("Query: %s", query)
        search_results = self.search(query=query)
        tags = []
        vr_elements = []
        for vr in search_results.docs:
            doc = json.loads(vr.json)
            tags.append(doc['Tag'])
            vr_elements.append(doc)

        summary = ""
        for tag in set(tags):
            for vr in vr_elements:
                if vr['Tag'] == tag:
                    summary += f"{vr}\n"
                    break
        return summary
    
    def _validate_content(self, data):
        try:
            converted_data = json.loads(data.model_dump_json())
            logging.debug("Saving content in Redis %s: ", converted_data)
            return converted_data
        except: 
            return data
        
    def _validate_id(self, id):
        if(id):
            return id
        return f"{config.VR_KEY_PREFIX}{str(uuid.uuid4())}"