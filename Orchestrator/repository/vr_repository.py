from config.db import get_redis_db_client
from config.environment import config
import logging

logging.basicConfig(level=logging.DEBUG)
logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class VRRepository():
    def __init__(self):
        self.redis_client = get_redis_db_client()

    def saveAll(self, return_saved=False, vr_states=[]):
        modified_ids = []
        for vr_state in vr_states:
            id = f"{config.KEY_PREFIX}{vr_state['Id']}"
            modified_ids.append(id)
            self._save_single_object(id=id, property="$", vr_state=vr_state)
        if return_saved:
            return self._find_ids(modified_ids=modified_ids)

    def _save_single_object(self, id, property, vr_state):
        self.redis_client.json().set(id, property, vr_state)
    
    def _find_ids(self, ids):
        modified_vr_objects = []
        for id in ids:
            modified_vr_objects.append(self.redis_client.json(id).get(id))
            logging.debug("[updateAllWithTemplate] VR Status found: %s", self.redis_client.json(id).get(id))
        return modified_vr_objects
    
    def updateAllWithTemplate(self, return_saved=False, template=None):
        logging.debug("[updateAllWithTemplate] query: %s", template.search_query)
        search_results = self.redis_client.ft(config.INDEX_NAME).search(template.search_query)

        modified_ids = []
        for doc in search_results.docs:
            for doc_update in template.properties_to_update:
                logging.debug("[updateAllWithTemplate] doc_update.property: %s, doc_update.value: %s", doc_update.property, doc_update.value)
                self.redis_client.json().set(doc.id, doc_update.property, doc_update.value)
                modified_ids.append(doc.id)

        if return_saved:
            return self._find_ids(modified_ids)
