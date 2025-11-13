import boto3
import json
import logging
import redis
import os
from config.environment import config
logging.basicConfig(level=logging.DEBUG)
logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def connect_redis_vr_state():
  
  client = redis.StrictRedis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        password=config.REDIS_PASSWORD,
        decode_responses=True,
        # ssl=True,
    )