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

    async def save_all(self, return_saved=False, content=[]):
        saved_ids = []
        for state in content:
            id = self._format_id()
            saved_ids.append(id)
            await self.save_one(id=id, property="$", content=state)
        logging.info("%s units saved", len(saved_ids))
        if return_saved:
            return await self._find_ids(modified_ids=saved_ids)

    async def save_one(self, id=None, property="$", content=None):
        self.redis.client.json().set(id, property, content)
    
    async def _find_ids(self, ids):
        modified_vr_objects = []
        for id in ids:
            modified_vr_objects.append(self.redis.client.json(id).get(id))
            logging.debug("Unit found: %s", self.redis.client.json(id).get(id))
        return modified_vr_objects
    
    async def update_all(self, return_saved=False, content=None):
        logging.debug("Updating units: %s", content)
        search_results = self.search(query=content['search_query'])

        modified_ids = []
        for doc in search_results.docs:
            for doc_update in content["properties_to_update"]:
                self.redis.client.json().set(doc.id, doc_update["property"], doc_update["value"])
                modified_ids.append(doc.id)

        logging.info("%s units updated", len(modified_ids))
        if return_saved:
            return await self._find_ids(modified_ids)
    
    def search(self, query="-@Tag:{agent_history | detailed_state | summarized_state}"):
        search_query = Query(query).paging(offset=0, num=config.REDIS_SEARCH_LIMIT)
        return self.redis.client.ft(config.VR_INDEX).search(search_query)
    
    def search_chat_history(self, query="@Tag:{agent_history}"):
        search_results = self.search(query=query)
        chat_history = []
        keys_schema = ["Role", "Content"]
        for data in search_results.docs:
            chat_history.append({key.lower(): json.loads(data.json)[key] for key in keys_schema})
        return chat_history
    
    async def cache_real_time_state(self):
        # This realtime state summary contains less data and is more suitable to be bassed to the agent as context

        # First the cached elements are deleted, and then recreated
        search_results = self.search("@Tag:{summarized_state}")
        for vr in search_results.docs:
            self.redis.client.unlink(vr.id)

        # Search all 3D object's items
        search_results = self.search()
        unique_tags = []
        for vr in search_results.docs:
            doc = json.loads(vr.json)
            tag = doc.get('Tag', '').casefold().replace(" ", "")
            if tag not in unique_tags:
                await self.save_one(id=self._format_id(), content=self._format_summarized_item(doc))
                unique_tags.append(tag)
        logging.debug("Items saved: %s", unique_tags)

    def _format_summarized_item(self, vr=None):
        FORCE_LIMIT = 9.83
        TORQUE_LIMIT = 4.76

        name = vr['Tag'].capitalize() if vr['Tag'] else None
        color = vr['Components']['Color'].capitalize() if vr.get('Components', {}).get('Color') else None
        scale = vr.get('Transform', {}).get('Reshape', None)
        size = "bigger size" if scale >= 1.1 else ("smaller size" if scale <= 0.9 else "normal size")
        gravity = ""
        rotation = ""
        constant_force = vr.get('Components', {}).get('ConstantForce')
        if constant_force:
            gravity = "levitating" if constant_force.get("Force", {}).get("Y", None) >= FORCE_LIMIT else "not levitating"
            rotation = "rotating" if constant_force.get("RelativeTorque", {}).get("X", None) >= TORQUE_LIMIT else "not rotating"
        
        return { 
            "Tag": "summarized_state", 
            "name": name, 
            "color": color, 
            "gravity": gravity, 
            "rotation": rotation,
            "size": size}
    
    def search_system_statistics(self):
        # This real time state much data and is not passed as the agent context, but rather it is accessed in a function tool
        search_results = self.search()
        real_time_states = []
        for doc in search_results.docs:
            real_time_states.append(doc)

        logging.debug("Found %s detailed items", len(real_time_states))
        return {"role": "assistant", 
                "content": f"The following is the detailed 3D state of the elements for statistics: {real_time_states}"}

    def get_real_time_summary(self):
        search_results = self.search("@Tag:{summarized_state}")
        real_time_summary = []
        for doc in search_results.docs:
            real_time_summary.append(doc)

        logging.debug("Found %s summarized items", len(real_time_summary))
        return {"role": "assistant", 
                "content": f"The following is the summary of the current state of the 3D elements: {real_time_summary}"}


    def _format_id(self, id=None):
        if id:
            return f"{config.VR_KEY_PREFIX}{id}"
        else:
            return f"{config.VR_KEY_PREFIX}{str(uuid.uuid4())}"
    
    async def purge_all(self, query="*"):
        logger.debug("Scanning for existing cache")
        cache = list(self.redis.client.scan_iter(query))
        if len(cache) < 1:
            logger.debug("No cache found")
            return
        for key in cache:
            self.redis.client.delete(key)
        logger.debug("Cache successfully deleted")