import logging
import json
logging.basicConfig(level=logging.DEBUG)
logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def get_formatted_vr_state(template):
    logger.debug("[get_formatted_vr_state] Received template: %s", template["template"])
    conf = {"properties_to_update": []}
    query = ""
    
    for line in template["template"].split("\n"):
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
    return json.dumps(conf)