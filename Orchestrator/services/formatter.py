import logging
from models.vr_config_props import VRModificationConfig, VRUpdateConfig

logging.basicConfig(level=logging.DEBUG)
logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def get_formatted_config(template):
    logger.debug("[get_formatted_config] Received template: %s", template)
    query = ""
    properties = []
    
    for line in template.split("\n"):
        if len(line.strip()) == 0:
            continue
        if "@" == line.strip()[0] and "[]" not in line and "{}" not in line:
            query = f"{query} {line}".strip()
        if "$" == line.strip()[0]:
            update = line.split("=")
            vrupdate_config = VRUpdateConfig()
            vrupdate_config.property = update[0].strip()
            try:
                vrupdate_config.value = float(update[1].strip())
            except:
                vrupdate_config.value = update[1].strip()
            properties.append(vrupdate_config)
    
    conf = VRModificationConfig()
    conf.search_query = query
    conf.properties_to_update = properties
    return conf