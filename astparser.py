from scratchast import scratchast
from sb3unzipper import sb3unzipper
import json
import collections

class astparser:

    def __init__(self):
        self.scratchast_class = scratchast() 
        self.ast_dict = {}
        self.all_keys = []
        self.ast_dict1 = {}
        self.parsed_value = None
        self.sb3class = sb3unzipper()
        self.json_data = None

    def dissect_scratch(self,json_value):

        if json_value is None:
            return None
        
        if isinstance(json_value,dict) and bool(json_value):
            for key,value in json_value.items():
                if isinstance(value,dict) and bool(value):
                    self.dissect_scratch(value)
                elif isinstance(value,list) and len(value) > 0:
                    for each_val in value:
                        self.dissect_scratch(each_val)
                elif isinstance(value,str) or isinstance(value,int) or isinstance(value,bool):
                    #self.scratchast_class.scratchdtype = self.scratchast_class.get_target_word_datatype(value)
                    #self.scratchast_class.scratchpreceding = key
                    #self.scratchast_class.value = value
                    #.ast_dict['datatype'] = self.scratchast_class.scratchdtype
                    #self.ast_dict['preceeding'] = self.scratchast_class.scratchpreceding
                    #self.ast_dict['value'] = self.scratchast_class.value
                    #self.ast_dict[key] = value

                    print(key,'->>',value)

                    #print(key,'->>' , value)
            
            
                
        elif isinstance(json_value,list) and len(json_value) > 0:
            for list_value in json_value:
                self.dissect_scratch(list_value)
        elif isinstance(json_value,str) or isinstance(json_value,int) or isinstance(json_value,bool) or json_value is None or json_value == None:
            #self.scratchast_class.scratchdtype = self.scratchast_class.get_target_word_datatype(json_value)
            #self.scratchast_class.scratchpreceding = json_value
            #self.scratchast_class.value = json_value
            #self.ast_dict['datatype'] = self.scratchast_class.scratchdtype
            #self.ast_dict['preced'] = self.scratchast_class.scratchpreceding
            #self.ast_dict['value'] = self.scratchast_class.value
            #print(self.ast_dict)
            print('json_value')

    def dissect_blocks(self,json_val):
        main_val = None
        if json_val is None:
            return None
        else:
            if isinstance(json_val,dict) and bool(json_val):
                main_val = json_val['targets']
                print(main_val)
        #return main_val

    def read_file(self,file_name):
        self.parsed_value = self.sb3class.unpack_sb3(file_name)
        self.json_data = json.loads(self.parsed_value)
        val = self.dissect_blocks(self.json_data)
        print(val)

astparser_class = astparser()
astparser_class.read_file("files/simple.sb3")
#astparser_class.dissect_blocks("files/sam.sb3")