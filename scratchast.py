class scratchast:

    def __init__(self):
        self.scratchdtype = None
        self.scratchpreceding = None
        self.value = None
    
    def get_scratch_dtype(self):
        return self.scratchdtype
    
    def get_scratch_preceding(self):
        return self.scratchpreceding
    
    def get_scratch_val(self):
        return self.value

    
    
    def get_target_word_datatype(self,target_word):

        if target_word is None:
            return "Unknown"
        else:
            if isinstance(target_word,dict):
                target_word_dtype = "Object"
            elif isinstance(target_word,list):
                target_word_dtype = "Array"
            elif isinstance(target_word,int):
                target_word_dtype = "Number"
            elif isinstance(target_word,str):
                target_word_dtype = "Literal"
            elif isinstance(target_word,bool):
                target_word_dtype = "Boolean"
            else:
                target_word_dtype = "Unknown"
            return target_word_dtype