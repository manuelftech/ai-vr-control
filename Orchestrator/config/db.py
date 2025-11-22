from config import config
import redis

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
        try:
            return redis.StrictRedis(
                host=config.REDIS_HOST,
                port=config.REDIS_PORT,
                password=config.REDIS_PASSWORD,
                decode_responses=True,
            )
        except Exception as e:
            raise Exception(e)
        
    def get_status(self):
        return self.connection_status
    
    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = super(RedisClient, cls).__new__(cls)
        return cls._singleton
    
    def _clean_cache(self):
        for key in self.client.scan_iter('*'):
            self.redis.client.delete(key)