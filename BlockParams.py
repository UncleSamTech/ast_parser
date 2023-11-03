class BlockParams:

    def __init__(self):
        self.params_key = None
        self.params_value = None


    def get_params_key(self):
        return self.params_key
    
    def get_params_value(self):
        return self.params_value
    
    def set_params_key(self,params_key):
        self.params_key = params_key

    def set_params_value(self,params_value):
        self.params_value = params_value
        