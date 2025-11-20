import json

class _VirtualRealityTool():
    """
    Manages the virtual environment, updating its state using a Redis Database
    """
    def _get_function(self, input):
        conf = {"properties_to_update": []}
        query = ""
        
        for line in input["template"].split("\n"):
            if len(line.strip()) == 0:
                continue
            if "@" == line.strip()[0] and "[]" not in line and "{}" not in line:
                query = f"{query} {line}".strip()
            if "$" == line.strip()[0]:
                update = line.split("=")
                properties_to_update = {}
                properties_to_update["property"] = update[0].strip()
                try:
                    properties_to_update["value"] = float(update[1].strip())
                except:
                    properties_to_update["value"] = update[1].strip()
                conf["properties_to_update"].append(properties_to_update)
        
        conf["search_query"] = query
        return conf

    def _get_definition(self):
         return {
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
            }