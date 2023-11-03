class BlocksClass:

    def __init__(self,opcode,params):
        self.opcode = opcode
        self.block_params = params
        

    def get_opcode(self):
        return self.opcode
    
    def get_block_params(self):
        return self.block_params
    
    def set_opcode(self,opcode):
        self.opcode = opcode

    def set_block_params(self,block_params):
        self.block_params = block_params

    
