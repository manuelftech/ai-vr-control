from redis.commands.search.query import Query
from config.redis_db import RedisClient
from config.config_vars import config
from dict_deep import deep_set
import uuid
import json
import structlog
from core.utils import update_nested_key
logger = structlog.get_logger()

class StateRepository():
    def __init__(self):
        self.redis = RedisClient()

    async def save(self, content, conversation_id):
        for state in content:
            doc = {"Tag": state.pop("Tag"), "ConversationId": conversation_id, "data": json.dumps(state)}
            self.redis.client.hset(f"{config.VR_KEY_PREFIX}{str(uuid.uuid4())}", mapping=doc)
        logger.info("%s units saved", len(content))
    
    async def update(self, content, conversation_id):
        logger.debug("Updating units: %s", content)
        search_results = self.search(tag=content.Tag, conversation_id=conversation_id)
        for doc in search_results.docs:
            data = json.loads(doc.data)
            for prop in content.Properties:
                deep_set(data, prop.Name, prop.State)
            self.redis.client.hset(doc['id'], mapping={
                "Tag": content.Tag, 
                "ConversationId": conversation_id,
                "data": json.dumps(data)})
        logger.info("%s units updated", len(search_results.docs))

    def search(self, tag=None, conversation_id=None):
        search_items = []
        if tag:
            search_items.append(f"{config.TAG_SEARCH}{{{tag}}}")
        if conversation_id:
            search_items.append(f"{config.CONVERSATION_ID_SEARCH}{{{conversation_id}}}")

        query = Query(" ".join(search_items)).paging(offset=0, num=config.REDIS_SEARCH_LIMIT)
        return self.redis.client.ft(config.VR_INDEX).search(query)

    async def delete(self, conversation_id):
        logger.debug("Scanning for existing cache")
        search_results = self.search(conversation_id=conversation_id)
        if len(search_results.docs) < 1:
            logger.debug("No cache found")
            return
        for doc in search_results.docs:
            self.redis.client.delete(doc['id'])
        logger.debug("Deleted %s items", len(search_results.docs))