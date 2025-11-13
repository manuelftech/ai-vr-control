from config import db
from config import environment

class VRRepository():
    def _get_client(self):
        client = db.connect_redis_gameobjects()
        return client

    def saveAll(self, return_result=False, vr_states=[]):
        client = self._get_client()
        modified_ids = []
        for vr_state in vr_states:
            id = f"{environment.config.KEY_PREFIX}{vr_state['Id']}"
            modified_ids.append(id)
            self._save_single_object(client=client, id=id, property="$", vr_state=vr_state)
        if return_result:
            return self._find_ids(client, modified_ids)

    def _save_single_object(self, client, id, property, vr_state):
        client.json().set(id, property, vr_state)
    
    def _find_ids(self, client, ids):
        modified_vr_objects = []
        for id in ids:
            modified_vr_objects.append(client.json(id).get(id))
        return modified_vr_objects
    
    def updateAllWithTemplate(self, return_result=False, template=None):
        client = self._get_client()
        search_results = client.ft(environment.config.INDEX_NAME).search(template.search_query)

        modified_ids = []
        for doc in search_results.docs:
            for doc_update in template.properties_to_update:
                client.json().set(doc.id, doc_update.property, doc_update.value)
                modified_ids.append(doc.id)

        if return_result:
            return self._find_ids(client, modified_ids)
