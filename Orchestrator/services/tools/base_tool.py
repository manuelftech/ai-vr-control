class _Tool():
    def __init__(self, function_name):
        # We set the function name
        self.function_name = function_name
        # We obtain the function logic
        self.function = self._get_function
        # We obtain the JSON definition of the function to be called
        self.definition = self._get_definition()

    def _get_function(self):
        raise NotImplementedError("This class must be inherited") 
               
    def _get_definition(self):
        raise NotImplementedError("This class must be inherited")
