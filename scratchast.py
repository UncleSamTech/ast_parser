class scratchast:

    def __init__(self):
        self.scratchlinenumber = None
        self.scratchdtype = None
        self.scratchpreceding = None

    def get_scratch_linenumber(self):
        return self.scratchlinenumber
    
    def get_scratch_dtype(self):
        return self.scratchdtype
    
    def get_scratch_preceding(self):
        return self.scratchpreceding
    
    def get_line_count(self,file_name,target_word):
        line_no = 0
        target_word_list = []
        if file_name is None or target_word is None:
            return None
        with open(file_name,'r') as open_file:
            for each_code_line in open_file:
                line_no += 1
                if target_word in each_code_line:
                    target_word_list.append(target_word)
                    target_word_list.append(line_no)
        return target_word_list

    def get_target_word_datatype(self,target_word):
        target_word_dtype = None
        if target_word is None:
            return None
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

def test():
    scratchast_test = scratchast()
    print(scratchast_test.get_line_count("files/actual_response.json","currentCostume"))

test()