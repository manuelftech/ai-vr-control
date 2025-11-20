class _Tool():
    def __init__(self):
        self.function = self._get_function()
        self.definition = self._get_definition()

    def _get_function(self, input):
        raise NotImplementedError("This class must be inherited") 
               
    def _get_definition(self):
        raise NotImplementedError("This class must be inherited")
