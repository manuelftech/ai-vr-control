from config.environment import config
import redis

class RedisClient():
    def __init__(self):
        self.client = self.connect()
        self.connection_status = "Connected"

    def connect(self):
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

redis_db = RedisClient()