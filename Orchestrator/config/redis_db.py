from config.config_vars import config
import redis
import structlog
logger = structlog.get_logger()

class RedisClient():
    _singleton = None
    _is_already_initialized = False

    def __init__(self):
        if not self._is_already_initialized:
            self.client = self._connect()
            self._is_already_initialized = True

    def _connect(self):
        logger.debug("Connecting to Redis Database")
        try:
            redis_client = redis.StrictRedis(
                host=config.REDIS_HOST,
                port=config.REDIS_PORT,
                password=config.REDIS_PASSWORD,
                decode_responses=True,
            )
            if redis_client.ping():
                logger.debug("Connected to Redis Database")
                return redis_client
            raise Exception("Redis connection failed")
        except Exception as e:
            raise Exception(e)
    
    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(RedisClient, cls).__new__(cls)
        return cls._singleton