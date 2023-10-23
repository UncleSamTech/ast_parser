import os
import json
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
        return [v[key] for v in blocks_values if isinstance(v,dict) and bool(v)]
    
    def get_block_without_opcode(self,block_values,key):
        
        retr_block = self.get_any_block_by_id(block_values,key)
        return {k2:v2 for v in retr_block  for k2,v2 in v.items() if isinstance(v,dict) and bool(v) and k2 not in self.ommited_block_keys_parent}

    def build_line_display_tree(self,blocks_values,all_opcode):
        if isinstance(blocks_values,list)  and len(blocks_values) > 0:
            print(f'|---{all_opcode[0]}')
            for each_block in blocks_values:
               if isinstance(each_block,dict) and self.get_dict_depth(each_block) > 1:
                     for v in each_block.values():
                          
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


    def assign_val_to_sec_lev_tree(self,opcode_list,all_block_values):
        new_dict = {}
        sec_tree = self.create_second_level_tree_line(opcode_list)
        
        return sec_tree
    
    def read_files(self, parsed_file):
        if os.path.exists(parsed_file):
            with open(parsed_file, "r") as json_file:
                self.blocs_json = json.load(json_file)
            self.all_targets_value = self.get_all_targets(self.blocs_json)
            self.blocks_values = self.get_all_blocks_values(self.all_targets_value)
            
            all_opcode = self.return_all_opcode(self.blocks_values)
            #tr_line = self.create_tree_with_lines(self.join_opcode_and_block_id(self.blocks_values),self.blocks_values,all_opcode[0])
            #print(tr_line)
            #sec_tr = self.create_second_level_tree_line(self.join_opcode_and_block_id(self.blocks_values),self.blocks_values)
            #tr_lisp = self.create_tree_with_lisp(self.join_opcode_and_block_id(self.blocks_values),self.blocks_values,all_opcode[0])
            ln_disp = self.build_line_display_tree(self.blocks_values,all_opcode)
            tab_disp = self.build_tab_display_tree(self.blocks_values,all_opcode)
            #par = self.merge_parent_tree(all_opcode,sec_tr)
            print(tab_disp)
        
        else:
            print("File not found")

simple_parser_obj = simple_parser()
simple_parser_obj.read_files("files/actual_response.json")