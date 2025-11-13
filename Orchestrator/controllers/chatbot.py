from openai import OpenAI
import json

api_key = "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"
model = "gpt-5-nano"
client = OpenAI(api_key=api_key)

prompt = """
    take the following Redis Query template: 
    'Query:'
    @Tag:{} 
    @ComponentColor:{} 
    @ComponentConstantForceY:[]

    'Properties:'
    $.Components.ConstantForce.Y = 0
    $.Components.Color = '' 

    Answer only with that template
    The template is divided in two sections, Query and Properties
    The text starting with @ in the template refers to the Queries to find objects
    the text starting with $ refers to the future values that will be assigned to the objects

    You will identify the objects that need to be found, and replace those values for those in the Query template, and then find the new values to be assidned and replace them in the properties section of the template

    Example:
    1) If you are asked the following:
    'Make all green cubes float'
    You have to convert it to the following resulting template:
    @Tag:{cube} 
    @ComponentColor:{green}
    $.Components.ConstantForce.Y = 9.83

    2) If you are asked the following:
    'I want all cubes TO fall to the ground'
    You have to convert it to the following resulting template:
    @Tag:{cube}
    $.Components.ConstantForce.Y = 0

    3) If you are asked the following:
    'I need all floating cubes become blue'
    You have to convert it to the following resulting template:
    @Tag:{cube} 
    @ComponentConstantForceY:[+inf 9.83]
    $.Components.Color = 'blue'

    4) If you are asked the following:
    'I need all floating cubes that are yellow to become orange and to stop levitating'
    You have to convert it to the following resulting template:
    @Tag:{cube} 
    @ComponentConstantForceY:[+inf 9.83] 
    @ComponentColor:{yellow}
    $.Components.Color = 'orange'
    $.Components.ConstantForce.Y = 0

    Have in mind that if a property is not mentioned for searching, you should not include it in the response template
    the same applies for the properties to update, if they are not mentioned, do not return them.

    Answer the user:
"""

tools = [
    {
        "type": "function",
        "name": "get_formatted_gameobjects",
        "description": "Format your response for proper handling",
        "parameters": {
            "type": "object",
            "properties": {
                "sign": {
                    "type": "string",
                    "description": "A template with a Redis Query and properties to update",
                },
            },
            "required": ["template"],
        },
    },
]


# Create a running input list we will add to over time
input_list = [
    {"role": "user", "content": f"{prompt} I desire you to make float all purple chairs"}
]

# 2. Prompt the model with tools defined
response = client.responses.create(
    model=model,
    #tools=tools,
    input=input_list,
)

def get_formatted_gameobjects(template):
    """
    @Tag:{cube}
    @ComponentColor:{purple}
    $.Components.ConstantForce.Y = 9.83
    """

    queries = []
    for line in template.splitlines():
        if "@" in line:
            query = line

    search_query = ""
    conf = get_query_config(search_query)
    properties_to_update = get_properties_to_update()
    conf.properties_to_update = properties_to_update
    return conf

# Save function call outputs for subsequent requests
input_list += response.output

for item in response.output:
    if item.type == "function_call":
        if item.name == "get_formatted_gameobjects":
            # 3. Execute the function logic for get_horoscope
            gameobjects = get_formatted_gameobjects(json.loads(item.arguments))
            
            # 4. Provide function call results to the model
            input_list.append({
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": json.dumps({
                  "gameobjects": gameobjects
                })
            })

print("Final input:")
print(input_list)

response = client.responses.create(
    model=model,
    instructions="Return a Redis Query and property template.",
    tools=tools,
    input=input_list,
)

# 5. The model should be able to give a response!
print("Final output:")
print(response.model_dump_json(indent=2))
print("\n" + response.output_text)

def get_redis_search_query(filter):
    return "@Tag:{cube}"

def get_properties_to_update():
    from typing import Union

    class GameUpdateConfig:
        property: str
        value: Union[str | float]

def get_query_config(search_query):
    from typing import Union

    class GameUpdateConfig:
        property: str
        value: Union[str | float]

    class GameModificationConfig():
        search_query: str
        properties_to_update: list[GameUpdateConfig]
    
    conf = GameModificationConfig()
    conf.search_query = search_query
    conf.properties_to_update = []
    return conf