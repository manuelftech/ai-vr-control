from services.tools.real_time_states_tool import real_time_states_tool
from services.tools.documentation_details_tool import documentation_details_tool
from types import SimpleNamespace

class ToolManager():
    """
    Manages the set of tools to use within the agent workflow
    """
    def __init__(self):
        self.tools = [
            documentation_details_tool,
            real_time_states_tool
        ]

tool_manager = ToolManager()