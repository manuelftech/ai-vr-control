from openai import OpenAI
from config.environment import config
import json

def ask_chatbot(prompt):
    model = "gpt-4o-mini"
    client = OpenAI(api_key=config.LLM_API_KEY)

    prompt_config = """
        take the following Redis Query template: 
        'Query:'
        @Tag:{} 
        @ComponentColor:{} 
        @ComponentConstantForceY:[]

        'Properties:'
        $.Components.ConstantForce.Y = 0
        $.Components.Color = #FF0000 

        Answer only with that template
        The template is divided in two sections, Query and Properties
        The text starting with @ in the template refers to the Queries to find objects
        the text starting with $ refers to the future values that will be assigned to the objects

        You will identify the objects that need to be found, and replace those values for those in the Query template, and then find the new values to be assidned and replace them in the properties section of the template
        The first phrases of the user's question may start with 'make', 'I want', 'I desire', or somilar phrases, you have to take from those phrases the Query to find the @ elements,
        After that first phrase, if you read 'become', 'turn them', 'make', you will not assign those values to the Query, but to the properties, because it means these will be the new values that will be used in the properties
        Every time you add a property for color, it has to be the hexadecimal color code representation of the color, if you refer to a color on the Query part of the template, always add a \ before.

        Example:
        1) If you are asked the following:
        'Make all green cubes float'
        You have to convert it to the following resulting template:
        @Tag:{cube} 
        @ComponentColor:{\#00FF00}
        $.Components.ConstantForce.Y = 9.83

        2) If you are asked the following:
        'I want all chairs to fall to the ground'
        You have to convert it to the following resulting template:
        @Tag:{chair}
        $.Components.ConstantForce.Y = 0

        3) If you are asked the following:
        'I need all floating cubes become blue'
        You have to convert it to the following resulting template:
        @Tag:{cube} 
        @ComponentConstantForceY:[9.83 +inf ]
        $.Components.Color = #0000FF

        4) If you are asked the following:
        'I need all floating cubes that are yellow to become orange and to stop levitating'
        You have to convert it to the following resulting template:
        @Tag:{cube} 
        @ComponentConstantForceY:[9.83 +inf ] 
        @ComponentColor:{\#FFFF00}
        $.Components.Color = #FFA500
        $.Components.ConstantForce.Y = 0

        Have in mind that if a property is not mentioned for searching, you should not include it in the response template
        the same applies for the properties to update, if they are not mentioned, do not return them.

        After doing all of that, use the tool provided called get_formatted_vr_state and pass as input the returned template
        Answer the user:
    """

    tools = [
        {
            "type": "function",
            "name": "get_formatted_vr_state",
            "description": "Format your response for proper handling",
            "parameters": {
                "type": "object",
                "properties": {
                    "template": {
                        "type": "string",
                        "description": "A template with a Redis Query and properties to update",
                    },
                },
                "required": ["template"],
            },
        },
    ]

    def get_formatted_vr_state(template):
        print(f"[Validation] Received template: {template}")
        """```
        Query:
        @Tag:{cube} 
        @ComponentColor:{\#808080}
        @ComponentConstantForceY:[]
    
        Properties:
        $.Components.Color = #00FF00
        $.Components.ConstantForce.Y = 9.83
        ```"""
        return template["template"]

    # prompt = I desire you to make float all cubes and turn them green
    input_list = [
        {"role": "user", "content": f"{prompt_config} {prompt}"}
    ]

    response = client.responses.create(
        model=model,
        tools=tools,
        input=input_list
    )

    input_list += response.output

    for item in response.output:
        if item.type == "function_call":
            if item.name == "get_formatted_vr_state":
                vr_state = get_formatted_vr_state(json.loads(item.arguments))

                input_list.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps({
                      "vr_state": vr_state
                    })
                })

    print("Final input:")
    print(input_list)

    response = client.responses.create(
        model=model,
        instructions="Respond only with a Redis template generated by a tool.",
        tools=tools,
        input=input_list,
    )

    print("Final output:")
    print(response.model_dump_json(indent=2))
    print("\n" + response.output_text)

    return response.output_text