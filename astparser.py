from scratchast import scratchast
from sb3unzipper import sb3unzipper
import json
from TreeClass import TreeClasser
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

    def dissect_targets(self,json_val):
        return json_val['targets'] if isinstance(json_val,dict) and bool(json_val) else None
    
    
    def dissect_target_values(self, target_value):
        if isinstance(target_value,list) and len(target_value) > 0:
            for each_content in target_value:
                print(each_content)
        #return target_value[0:] if isinstance(target_value,list) and len(target_value) > 0 else []

    def get_top_keys(self,json_val):
        return json_val.keys() if isinstance(json_val,dict) and bool(json_val) else []

    def get_top_values(self,json_val):
        return json_val.values() if isinstance(json_val,dict) and bool(json_val) else []
    


    def create_simple_tree(self,json_val):
        tree_list = []
        if "targets" in self.get_top_keys(json_val):
            targ_cont = json_val["targets"]
            print(targ_cont)
            if isinstance(targ_cont,list) and len(targ_cont) > 0:
                for each_targ_cont  in targ_cont:
                    if isinstance(each_targ_cont,dict) and bool(each_targ_cont):
                        for key,value in each_targ_cont.items():
                           if isinstance(value,str) or isinstance(value,int) or isinstance(value,bool) or value == None or value == "":
                               print("targets=>",key,"<=",value)
                           else:
                               self.create_simple_tree(value)
                    #print("targets",each_targ_cont)
        return tree_list
        #for i in tree_list:

        

    def read_file(self,file_name):
        self.parsed_value = self.sb3class.unpack_sb3(file_name)
        self.json_data = json.loads(self.parsed_value)
        val = self.dissect_targets(self.json_data)
        keys = self.get_top_keys(self.json_data)
        #values = self.get_top_values(self.json_data)
        #target_values = self.dissect_target_values(self.dissect_targets(self.json_data))
        simp_tree = self.create_simple_tree(self.json_data)
        #print(keys)
        #print(target_values)
        #print(simp_tree)
        #print(values)

   

astparser_class = astparser()
tr_clas = TreeClasser("numbers")
tr_clas.setup_tree([2,3,4,5,6,7,7,3])
#astparser_class.read_file("files/simple.sb3")
#astparser_class.dissect_blocks("files/sam.sb3")