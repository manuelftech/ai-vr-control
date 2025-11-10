# import boto3
# import json
# import logging
# import os
# logging.basicConfig(level=logging.DEBUG)
# logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# logger = logging.getLogger(__name__)

# def get_item_from_dynamodb(rut):
#   # removing unwanted new lines or tab
#   rut = rut.strip('\n').strip('\t')
#   logging.info("Querying database using rut %s", rut)
#   dynamodb = boto3.client("dynamodb", region_name=os.environ.get("DATABASE_AWS_REGION"))
#   found_customer = dynamodb.get_item(TableName=os.environ.get("DYNAMODB_TABLE"), Key={os.environ.get("TABLE_PARTITION_KEY"):{'S':os.environ.get("TABLE_PARTITION_VALUE")}, 'rut':{'S': str(rut)}})
#   logging.debug("Item found in Database for rut %s: %s", rut, found_customer)
#   return found_customer['Item']

# def get_redis_connection():
#   import redis
#   import json

#   # USE_SSL = True 
#   client = redis.StrictRedis(
#         host=REDIS_HOST,
#         port=REDIS_PORT,
#         password=REDIS_PASSWORD,
#         # ssl=USE_SSL,
#         decode_responses=True 
#     )
#   try:
#     client.execute_command('FT.DROPINDEX', INDEX_NAME)
#     print(f"Index '{INDEX_NAME}' has been deleted successfully.")
#   except redis.exceptions.ResponseError as e:
#             print(f"Index '{INDEX_NAME}' not found. Creating index now...")

#             create_command_args = [
#                 'FT.CREATE', INDEX_NAME,
#                 'ON', 'JSON',
#                 'PREFIX', '1', f"{KEY_PREFIX}",
#                 'SCHEMA',
#                 '$.Id', 'AS', 'Id', 'TAG',
#                 '$.Tag', 'AS', 'Tag', 'TAG',
#                 '$.Name', 'AS', 'Name', 'TAG',
#                 '$.Components.ConstantForce', 'AS', 'ComponentsConstantForce', 'NUMERIC',
#                 '$.Components.Color', 'AS', 'ComponentsColor', 'TAG',
#                 '$.Transform.Position.X', 'AS', 'TransformPositionX', 'NUMERIC',
#                 '$.Transform.Position.Y', 'AS', 'TransformPositionY', 'NUMERIC',
#                 '$.Transform.Position.Z', 'AS', 'TransformPositionZ', 'NUMERIC',
#                 '$.Transform.Rotation.X', 'AS', 'TransformRotationX', 'NUMERIC',
#                 '$.Transform.Rotation.Y', 'AS', 'TransformRotationY', 'NUMERIC',
#                 '$.Transform.Rotation.Z', 'AS', 'TransformRotationZ', 'NUMERIC',
#                 '$.Transform.Scale.X', 'AS', 'TransformScaleX', 'NUMERIC',
#                 '$.Transform.Scale.Y', 'AS', 'TransformScaleY', 'NUMERIC',
#                 '$.Transform.Scale.Z', 'AS', 'TransformScaleZ', 'NUMERIC'
#             ]
            
#             client.execute_command(*create_command_args)
            
#             print(f"Successfully created index '{INDEX_NAME}'.")