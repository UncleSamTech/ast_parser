import os
import json
from sb3unzipper import sb3unzipper
import collections

class simple_parser:

    def __init__(self):

        self.all_targets_value = None
        self.blocs_json = None
        self.blocks_values = []
        self.blocks_tree = {}
        self.blocks_keys = []
        self.json_data_keys = None
        self.scratch_tree = {}
        self.parsed_value = None
        self.sb3class = sb3unzipper()
        self.opcode_parent_next = {}
        self.quick_opcpode_tree = {}

    ommited_block_keys_parent = {"opcode"}

    tree_depth_check = {'a':{'b':{'Message':['hello','2']},'c':'10','d':['how are you','3'],'e':{'cond':['x',5],'think':['x','20']}}}
    #print(tree_depth_check)

    def get_dict_depth(self,dict_data,depth=0):
        if not isinstance(dict_data,dict) or not dict_data:
            return depth
        return max(self.get_dict_depth(v,depth+1)  for k,v in dict_data.items())
    
    
    def check_non_nested_block(self,val):
        return isinstance(val,str) or val(int) or val(float) or val(bool) or val == None  
    
    
    def get_all_targets(self,json_data):
        if isinstance(json_data,dict) and bool(json_data):
            return json_data["targets"] if 'targets' in json_data.keys() else None

    def get_all_blocks_keys(self,targets_data): 
        if isinstance(targets_data,list) and len(targets_data) > 0:
            for each_target in targets_data:
                if isinstance(each_target,dict) and bool(each_target) and 'blocks' in each_target.keys():
                    self.blocks_keys.append(each_target['blocks'].keys())   
            return self.blocks_keys
        
    def get_all_blocks_values(self,targets_data):
        if isinstance(targets_data,list) and len(targets_data) > 0:
            block_values = [k['blocks'] for k in targets_data if isinstance(k,dict) and 'blocks' in k.keys()]
            return block_values
    
    def get_parent_node(self,blocks_values):
        return [values2 for v in blocks_values for values2 in v.values() if isinstance(v,dict) and bool(v)  and isinstance(values2,dict) and 'parent' in values2.keys() and values2['parent'] == None]
        
    def get_block_by_id_after_parent(self,blocks_values,key):
        return [v[key] for v in blocks_values if key.strip('') in v.keys()]
    
    def get_any_block_by_id(self,blocks_values,key):

        return [v[key] for v in blocks_values if isinstance(v,dict) and bool(v) and key != None or key != '' and key.strip('') in v.keys() and v[key] != None or v[key] != '']
    
    def get_block_byid(self,blocks,key):
        if isinstance(blocks,list) and len(blocks) > 0:
            for each_block in blocks:
                print(each_block)
                if  key == None or key == '' or key.strip('') not in each_block.keys():
                    return {}
                else:
                    print(each_block[key])
                    return each_block[key]
    def get_block_without_opcode(self,block_values,key):
        
        retr_block = self.get_any_block_by_id(block_values,key)
        return {k2:v2 for v in retr_block  for k2,v2 in v.items() if isinstance(v,dict) and bool(v) and k2 not in self.ommited_block_keys_parent}

    def get_opcode_of_parent_from_blockid(self,block_values,key):
        retr_block = self.get_any_block_by_id(block_values,key)
        return [v[k2] for v in retr_block for k2,v2 in v.items() if isinstance(v,dict) and bool(v) and k2 == 'opcode']

  
    
    def build_line_display_tree(self,blocks_values,all_opcode):
        if isinstance(blocks_values,list)  and len(blocks_values) > 0:
            print(f'|---{all_opcode[0]}')
            for each_block in blocks_values:
               if isinstance(each_block,dict) and self.get_dict_depth(each_block) > 1:
                     for k,v in each_block.items():
                          
                          print(f'  |---{v["opcode"]}' if v["parent"] != None else f"")
                          if  isinstance(v,dict) and self.get_dict_depth(v) > 1:
                              for k2,v2 in v.items(): 
                                  if isinstance(v2,dict) or isinstance(v2,list):
                                      self.build_line_display_tree(v2,all_opcode)
                                  else:
                                      print(f'    |---{k2}')
                                      print(f'      |---{v2}' if isinstance(v2,str) or isinstance(v2,int) or isinstance(v2,float) or isinstance(v2,bool) or v2 == None  else f'' )

    def build_tab_display_tree(self,blocks_values,all_opcode):
         if isinstance(blocks_values,list)  and len(blocks_values) > 0:
            print(f'{all_opcode[0]}')
            for each_block in blocks_values:
               if isinstance(each_block,dict) and self.get_dict_depth(each_block) > 1:
                     for v in each_block.values():
                          print(f'')
                          print(f'  {v["opcode"]}' if v["parent"] != None else f"")
                          if  isinstance(v,dict) and self.get_dict_depth(v) > 1:
                              for k2,v2 in v.items(): 
                                  if isinstance(v2,dict) or isinstance(v2,list):
                                      self.build_line_display_tree(v2,all_opcode)
                                  else:
                                      print(f'      {k2}')
                                      print(f'          {v2}' if isinstance(v2,str) or isinstance(v2,int) or isinstance(v2,float) or isinstance(v2,bool) or v2 == None  else f'' )    
        

    
                                    
    def get_all_block_keys(self,blocks_values):
        return [v.keys() for v in blocks_values if isinstance(v,dict) and bool(v)]
    
    def get_next_node_id(self,parent_block):
       return [value['next'] for value in parent_block  if isinstance(value,dict) and bool(value)  and 'next' in value.keys() and value['next'] != None]
    
    def get_any_node_id_from_block(self,block):
        return [value['next'] for value in block if isinstance(value,dict) and bool(value)  and 'next' in value.keys() and value['next'] != None]
    
    def get_opcode_from_block(self,block):
        return [block['opcode'] if isinstance(block,dict) and bool(block) and 'opcode' in block.keys() else None][0]
    
    def return_all_opcode(self,blocks_values):
        return [sub_block['opcode'] for each_block in blocks_values for sub_block in each_block.values() if isinstance(each_block,dict) and bool(each_block) and isinstance(sub_block,dict) and bool(sub_block) and 'opcode' in sub_block.keys()]
    
    
    def join_opcode_and_block_id(self,blocks_values):
        return [{sub_block['opcode']:sub_block_key} for each_block in blocks_values for sub_block_key,sub_block in each_block.items() if isinstance(each_block,dict) and bool(each_block) and isinstance(sub_block,dict) and bool(sub_block)]

    def join_opcodes_and_block_id_parent(self,blocks_values):
        return [{sub_block['opcode']:[sub_block_key,sub_block['parent'],self.get_opcode_of_parent_from_blockid(blocks_values,sub_block['parent'])]} for each_block in blocks_values for sub_block_key,sub_block in each_block.items() if isinstance(each_block,dict) and bool(each_block) and isinstance(sub_block,dict) and bool(sub_block) ]
    
    def get_all_bl_id(self,block_values):
        return [sub_block_key for each_block in block_values for sub_block_key,sub_block in each_block.items() if isinstance(each_block,dict) and bool(each_block) and isinstance(sub_block,dict) and bool(sub_block)]             
                         
                    
    def create_second_level_tree_line(self,opcode_id_list,blocks_values):
        return {k:self.get_block_without_opcode(blocks_values,v)  for opc_id in opcode_id_list[1:] if isinstance(opc_id,dict) and bool(opc_id) for k,v in opc_id.items()}
    

    def get_all_block_values(self,block_id_list,blocks_values):
        return [self.get_block_without_opcode(blocks_values,block) for block in block_id_list[1:] if isinstance(block_id_list,list) and len(block_id_list) > 0]

    def merge_parent_tree(self,opcode_list,second_level_tree):
        compl_tree = {opcode_list[0]:second_level_tree}
        print(f'|---{opcode_list[0]}')
        print(f'    |---{second_level_tree}')
        json_val = json.dumps(compl_tree)
        return json_val
    
    def get_block_opcode(self,blocks_values,key):
        joined_opcodes_block_id = self.join_opcodes_and_block_id_parent(blocks_values)
        for each_block in joined_opcodes_block_id:
            for k,v in each_block.items():
                if v[0] == key:
                    return k
                
    


    def quick_test(self,blocks_values,all_opcode):
        print(f'sprite')
        print('|')
        print(f'+---+{all_opcode[0]}')
        print(f'    |')
        if isinstance(blocks_values,list) and len(blocks_values) > 0:
            for each_value in blocks_values:
                if isinstance(each_value,dict)  and bool(each_value):
                    for key,value in each_value.items():
                        #parent_opcode = self.get_parent_opcode(blocks_values,key) if self.get_parent_opcode(blocks_values,key) != None or self.get_parent_node(blocks_values,key) != [] or self.get_parent_node(blocks_values,key) is not None else ''
                        print(f'    +---+{self.get_block_opcode(blocks_values,key)}' if value['parent'] != None  else f"")
                        print(f'        |')
                        #print(f'        +---+{self.get_block_opcode(blocks_values,key)}' if value['parent'] != None else f"")
                        #print(f'            |')
                        for k2,v2 in value.items():
                            if isinstance(v2,dict) or isinstance(v2,list):
                                self.quick_test(v2,all_opcode)
                            else:
                                print(f'        +---+{v2}')
                                #print(f'                |')
                                #print(f'                +---+{v2}' if isinstance(v2,str) or isinstance(v2,int) or isinstance(v2,float) or isinstance(v2,bool) or v2 == None  else f'')


    def get_needed_opcode_values(self,block_values):
        pass         

    def assign_val_to_sec_lev_tree(self,opcode_list,all_block_values):
        new_dict = {}
        sec_tree = self.create_second_level_tree_line(opcode_list)
        
        return sec_tree
    
    def get_opcode_from_id(self,block_values,block_id):
        if isinstance(block_values,list) and len(block_values) > 0:
            for each_block in block_values:
                if isinstance(each_block,dict) and bool(each_block) and block_id in each_block.keys():
                    return each_block[block_id]['opcode']
                
    def get_block_from_id(self,block_values,block_id):
        if isinstance(block_values,list) and len(block_values) > 0:
            for each_block in block_values:
                if isinstance(each_block,dict) and bool(each_block) and block_id in each_block.keys():
                    return each_block[block_id]
    
    def get_blockopcode_parent_opcode_next_opcode(self,blocks_values,block_id):
        block_by_id = self.get_any_block_by_id(blocks_values,block_id)[0]
        
        return {block_by_id['opcode']:[self.get_opcode_from_id(blocks_values,block_by_id['parent']),self.get_opcode_from_id(blocks_values,block_by_id['next'])] for key,value in block_by_id.items() if 'opcode' in key or 'parent' in key or 'next' in key}
    
    def create_quick_tree(self,blocks_values,all_opcode):
        main_parent_opcode = all_opcode[0]
        main_parent_id  = self.join_opcode_and_block_id(blocks_values)[0][main_parent_opcode]
        print(f'sprite')
        print('|')
        print(f'+---+{main_parent_opcode}')
        if isinstance(blocks_values,list) and len(blocks_values) > 0:
            for each_block in blocks_values:
                if isinstance(each_block,dict) and bool(each_block):
                    for k,v in each_block.items():
                        
                        current_block = self.get_block_from_id(blocks_values,k) if k != None else {}
                        next_block = self.get_block_from_id(blocks_values,v['next']) if v['next'] != None else {}
                        parent_block = self.get_block_from_id(blocks_values,v['parent']) if v['parent'] != None else {}
                        current_block_parent = current_block['parent']  if current_block != None else ''
                        if next_block == {} or next_block == None or next_block == '' or parent_block == {} or parent_block == None or parent_block == '' or current_block == {} or current_block == None or current_block == '':
                            continue
                        next_block_parent = next_block['parent']  if next_block != None or next_block != {} else ''
                        next_block_next = next_block['next'] if next_block != None or next_block != {} else ''
                        parent_block_parent = parent_block['parent'] if parent_block != None else ''
                        #print(f'{parent_block}  => {current_block} => {next_block} ')
                        #print(f'next block {next_block}')
                        #print(f'parent block {parent_block}')
                        current_opcode = self.get_opcode_from_id(blocks_values,k)    
                        parent_opcode = self.get_opcode_from_id(blocks_values,v['parent']) 
                        next_opcode = self.get_opcode_from_id(blocks_values,v['next'])
                        #print(f'currentid {k} current opcode -> {current_opcode} parent opcode -> {parent_opcode} next opcode -> {next_opcode}')
                        if current_opcode == main_parent_opcode:
                            continue
                        
                        #print(f' current parent {v["parent"]}')
                        #current block and same block have same parent
                        
                        
                        print(f'    |')
                        print(f'    +---+{current_opcode}')
                        print(f'        |')
                        print(f'        +---+{next_opcode if v["next"] == None else ""}')
                        
                        

    
    def draw_tree_current_next(self,blocks_values,all_opcode):
        print(f'sprite')
        print('|')
        print(f'+---+{all_opcode[0]}')
        if isinstance(blocks_values,list) and len(blocks_values) > 0:
            for value in blocks_values:
                if isinstance(value,dict)  and bool(value):
                    for k,v in value.items():
                        for k2,v2 in v.items():
                            if isinstance(v2,dict) or isinstance(v2,list):
                                self.draw_tree_current_next(v2,all_opcode)
                            else:
                                paren = self.get_opcode_from_id(blocks_values,v["parent"])
                                next_key = self.get_opcode_from_id(blocks_values,v["next"]) 
                                next_key_block = self.get_block_byid(blocks_values,v["next"])
                                print(next_key_block)
                                print(f'    |')
                                print(f'    +---+{paren if paren != None or paren != "" else ""}')
                                print(f'        |')
                                print(f'        +---+{v["opcode"]}' if v["parent"] != None else f"")
                                print(f'            |')
                                #print(f'        +---+{self.get_opcode_from_id(blocks_values,v["next"])}' if v["parent"] != None else f"")
                                print(f'                +---+{next_key if next_key != None or next_key != "" else ""}')
                                print(f'                    |')
                                print(f'                    +---+{k2}')
                                print(f'                        |')
                                print(f'                        +---+{v2}' if isinstance(v2,str) or isinstance(v2,int) or isinstance(v2,float) or isinstance(v2,bool) or v2 == None  else f'')

    def read_files(self, parsed_file):
        self.parsed_value = self.sb3class.unpack_sb3(parsed_file)
        self.blocs_json = json.loads(self.parsed_value)
        self.all_targets_value = self.get_all_targets(self.blocs_json)
        self.blocks_values = self.get_all_blocks_values(self.all_targets_value)
            
        #if os.path.exists(parsed_file):
            #with open(parsed_file, "r") as json_file:
                #self.blocs_json = json.load(json_file)
            #self.all_targets_value = self.get_all_targets(self.blocs_json)
            #self.blocks_values = self.get_all_blocks_values(self.all_targets_value)
            
        all_opcode = self.return_all_opcode(self.blocks_values)
        
            #tr_line = self.create_tree_with_lines(self.join_opcode_and_block_id(self.blocks_values),self.blocks_values,all_opcode[0])
            #print(tr_line)
            #sec_tr = self.create_second_level_tree_line(self.join_opcode_and_block_id(self.blocks_values),self.blocks_values)
            #tr_lisp = self.create_tree_with_lisp(self.join_opcode_and_block_id(self.blocks_values),self.blocks_values,all_opcode[0])
        #ln_disp = self.build_line_display_tree(self.blocks_values,all_opcode)
        #tab_disp = self.build_tab_display_tree(self.blocks_values,all_opcode)
        #bd = self.join_opcodes_and_block_id_parent(self.blocks_values)
        #qt = self.quick_test(self.blocks_values,all_opcode)
        #print(qt)
        #print(self.parsed_value)
        #print(self.blocks_values)
            #par = self.merge_parent_tree(all_opcode,sec_tr)

        #any_block = self.get_any_block_by_id(self.blocks_values,',r([,#`OV3[DwDfw/x./')
        #bl_opc = self.get_blockopcode_parent_opcode_next_opcode(self.blocks_values,'Ml@l~n|$+$jrg9V%IzC{')
        #dr_tr = self.draw_tree_current_next(self.blocks_values,all_opcode)
        #print(dr_tr)
        fil = self.create_quick_tree(self.blocks_values,all_opcode)

        print(fil)
        #print(tab_disp)
        #print(qt)
        #else:
            #print("File not found")
    

simple_parser_obj = simple_parser()
simple_parser_obj.read_files("files/test.sb3")