from config import config
import logging
import redis
logger = logging.getLogger(__name__)

class RedisClient():
    _singleton = None
    _is_already_initialized = False

    def __init__(self):
        if not self._is_already_initialized:
            self.client = self._connect()
            self.connection_status = "Connected"
            self._is_already_initialized = True
            self._clean_cache()

    def _connect(self):
        logger.debug("Connecting to Redis Database")
        try:
            redis_client = redis.StrictRedis(
                host=config.REDIS_HOST,
                port=config.REDIS_PORT,
                password=config.REDIS_PASSWORD,
                decode_responses=True,
            )
            logger.debug("Successfuly connected to Redis Database")
            return redis_client
        except Exception as e:
            raise Exception(e)
        
    def get_status(self):
        return self.connection_status
    
    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = super(RedisClient, cls).__new__(cls)
        return cls._singleton
    
    def _clean_cache(self):
        logger.debug("Scanning for cache elements for cleaning")
        cache = list(self.client.scan_iter('*'))
        if len(cache) < 1:
            logger.debug("No cache found")
            return
        for key in cache:
            self.client.delete(key)
            logger.debug("Cache deleted: Key %s", key)