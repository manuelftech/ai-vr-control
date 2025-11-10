import redis
import json

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
INDEX_NAME = "GameObjectsIdx"
KEY_PREFIX = "properties:"
REDIS_PASSWORD = "123456" 
# USE_SSL = True 
client = redis.StrictRedis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        # ssl=USE_SSL,
        decode_responses=True 
    )

""" Example prompt:
Make the red cubes float. Query: "@Tag:{cube} @ComponentsColor:{red} @ComponentsConstantForce:[-inf 9.82]"

Make the yellow cubes fall to the ground. Query: "@Tag:{cube} @ComponentsColor:{yellow} @ComponentsConstantForce:[+inf 9.82]"

make the chairs have less gravity, and also make the green cubes fall to the ground. These are two queries:
Query: "@Tag:{chair} @ComponentsConstantForce:[-inf 9.82]"
Query: "@Tag:{cubes} @ComponentsColor:{green} @ComponentsConstantForce:[-inf 9.82]"
"""

try:
    client.execute_command('FT.DROPINDEX', INDEX_NAME)
    print(f"Index '{INDEX_NAME}' has been deleted successfully.")
except redis.exceptions.ResponseError as e:
            print(f"Index '{INDEX_NAME}' not found. Creating index now...")

            create_command_args = [
                'FT.CREATE', INDEX_NAME,
                'ON', 'JSON',
                'PREFIX', '1', f"{KEY_PREFIX}",
                'SCHEMA',
                '$.Id', 'AS', 'Id', 'TAG',
                '$.Tag', 'AS', 'Tag', 'TAG',
                '$.Name', 'AS', 'Name', 'TAG',
                '$.Components.ConstantForce', 'AS', 'ComponentsConstantForce', 'NUMERIC',
                '$.Components.Color', 'AS', 'ComponentsColor', 'TAG',
                '$.Transform.Position.X', 'AS', 'TransformPositionX', 'NUMERIC',
                '$.Transform.Position.Y', 'AS', 'TransformPositionY', 'NUMERIC',
                '$.Transform.Position.Z', 'AS', 'TransformPositionZ', 'NUMERIC',
                '$.Transform.Rotation.X', 'AS', 'TransformRotationX', 'NUMERIC',
                '$.Transform.Rotation.Y', 'AS', 'TransformRotationY', 'NUMERIC',
                '$.Transform.Rotation.Z', 'AS', 'TransformRotationZ', 'NUMERIC',
                '$.Transform.Scale.X', 'AS', 'TransformScaleX', 'NUMERIC',
                '$.Transform.Scale.Y', 'AS', 'TransformScaleY', 'NUMERIC',
                '$.Transform.Scale.Z', 'AS', 'TransformScaleZ', 'NUMERIC'
            ]
            
            client.execute_command(*create_command_args)
            
            print(f"Successfully created index '{INDEX_NAME}'.")
            
request = {
            "Id": "abc123",
            "Tag": "cube",
            "Name": "Cube_2",
            "Components": {
                "ConstantForce": 9.82,
                "Color": "red"
            },
            "Transform": {
                "Position": {
                    "X": 1.98,
                    "Y": 1.287,
                    "Z": 1.331
                },
                "Rotation": {
                    "X": 0,
                    "Y": 0,
                    "Z": 5.17
                },
                "Scale": {
                    "X": 0.04014344,
                    "Y": 0.4354826,
                    "Z": 0.03871146
                },
            }
        }

client.json().set(f"{KEY_PREFIX}{request['Id']}" , '$', request)

#query = "@Tag:{cube} @ComponentsColor:{red} @ComponentsConstantForce:[-inf 9.82]"
query = "@Tag:{cube}"
search_results = client.ft(INDEX_NAME).search(query)
search_results

try:
    NEW_CONSTANT_FORCE_VALUE = 999
    updated_objects = []
    print(f"Found {search_results.total} objects to update.")
    for doc in search_results.docs:
        key = doc.id
        client.json().set(key, '$.Components.ConstantForce', NEW_CONSTANT_FORCE_VALUE)
        updated_json = client.json().get(key)
        updated_objects.append(updated_json)
        print(f"Updated key {key}, new force: {updated_json.get('constantforce')}")

    print("\n--- Summary of all updated objects (full JSON) ---")
    for obj in updated_objects:
        print(json.dumps(obj, indent=2))

except redis.exceptions.ResponseError as e:
    print(f"\nAn error occurred, likely related to the index configuration or search query syntax:")
    print(e)
except redis.exceptions.ConnectionError as e:
    print(f"\nCould not connect to Redis server. Ensure Redis Stack is running.")
    print(e)