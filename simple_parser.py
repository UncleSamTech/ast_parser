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

    ommited_block_keys_parent = {"opcode"}
    
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
        return [v[key] for v in blocks_values  if isinstance(v,dict) and bool(v) and key in v.keys()]
    
    def get_all_block_keys(self,blocks_values):
        return [v.keys() for v in blocks_values if isinstance(v,dict) and bool(v)]
    
    def get_next_node_id(self,parent_block):
       return [value['next'] for value in parent_block  if isinstance(value,dict) and bool(value)  and 'next' in value.keys() and value['next'] != None]
    
    def get_any_node_id_from_block(self,block):
        return [value['next'] for value in block if isinstance(value,dict) and bool(value)  and 'next' in value.keys() and value['next'] != None]
        
    #def get_next_block_by_id(self,blocks_values,id):
     
    def get_simple_tree(self,blocks_values):
            parent_node = self.get_parent_node(blocks_values)
            
            #ommit opcode and shadow keys
            next_block_afer_parent = {k:v for k,v in parent_node[0].items() if k not in self.ommited_block_keys_parent}
            print('parent_block',next_block_afer_parent)
            next_node_id_after_parent = self.get_next_node_id(parent_node)
            any_succeding_block = self.get_any_block_by_id(blocks_values,next_node_id_after_parent[0])
            print('next_block_after_parent',any_succeding_block)            
            subs_node_id = self.get_any_node_id_from_block(any_succeding_block)
            print('1subs_node_id',subs_node_id)
            self.blocks_tree = {parent_node[0]['opcode']:next_block_afer_parent}
            #while(subs_node_id != None):
                #self.blocks_tree.update({k:v for k,v in any_succeding_block[0].items() if k not in self.ommited_block_keys_parent})
                ##any_succeding_block = self.get_any_block_by_id(blocks_values,subs_node_id)
                #print('cont anyblock',any_succeding_block) 
                #subs_node_id = self.get_any_node_id_from_block(any_succeding_block)
                #print(subs_node_id)

            return self.blocks_tree
                       
                         
                    
                       
                           
            

    
    def read_files(self, parsed_file):
        if os.path.exists(parsed_file):
            with open(parsed_file, "r") as json_file:
                self.blocs_json = json.load(json_file)
            self.all_targets_value = self.get_all_targets(self.blocs_json)
            self.blocks_values = self.get_all_blocks_values(self.all_targets_value)
            
            #print(self.get_parent_node(self.blocks_values)[0])
            #print(self.get_next_node_id(self.get_parent_node(self.blocks_values))[0])
            print(self.get_simple_tree(self.blocks_values))
           # print(self.get_all_block_keys(self.blocks_values))
            #print(self.get_any_block_by_id(self.blocks_values,'1UL=3GeJ?mT{5;Vugp|2'))
        else:
            print("File not found")

simple_parser_obj = simple_parser()
simple_parser_obj.read_files("files/actual_response.json")