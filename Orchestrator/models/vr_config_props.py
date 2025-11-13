from typing import Union

class VRUpdateConfig:
        property: str
        value: Union[str | float]

class VRModificationConfig():
        search_query: str
        properties_to_update: list[VRUpdateConfig]