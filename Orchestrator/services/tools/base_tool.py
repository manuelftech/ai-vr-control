class _Tool():
    def __init__(self):
        # We obtain the function logic
        self.function = self._get_function
        # We obtain the JSON definition of the function to be called
        self.definition = self._get_definition()
        self.needs_additional_prompt = None

    def _get_function(self):
        raise NotImplementedError("This class must be inherited") 
               
    def _get_definition(self):
        raise NotImplementedError("This class must be inherited")
