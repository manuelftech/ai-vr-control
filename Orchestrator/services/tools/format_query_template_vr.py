from services.tools.base_tool import _Tool

class _FormatQueryVR(_Tool):
    """
    Manages the virtual environment, updating its state using a Redis Database
    """
    def __init__(self):
        super().__init__("format_query_template_vr")
    
    def _get_function(self, input):
        result = {"properties_to_update": []}
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
                result["properties_to_update"].append(properties_to_update)
        
        result["search_query"] = query
        result["continue_workflow"] = False
        return result

    def _get_definition(self):
         return {
                "type": "function",
                "name": self.function_name,
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