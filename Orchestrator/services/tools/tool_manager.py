from services.tools.real_time_states import _RealTimeStates
from services.tools.extract_project_details import _ExtractProjectDetails

class ToolManager():
    """
    Manages the set of tools to use within the agent workflow
    """
    def __init__(self):
        self.descriptions = self._configure_tools()
        if not self.descriptions:
            raise NotImplementedError("No function tools added")
        self.functions = [tool.definition for tool in self.definitions]

    def _configure_tools(self):
        # Add more tools as needed
        return [
            _RealTimeStates(),
            _ExtractProjectDetails(),
            ]