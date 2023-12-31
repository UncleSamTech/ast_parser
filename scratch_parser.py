import os
import json
from sb3unzipper import sb3unzipper

class scratch_parser:

    def __init__(self):
        
        self.blocs_json = None
        self.blocks_values = []
        self.sb3class = sb3unzipper()
        self.ommited_block_keys_parent = {"opcode"}
        self.all_opcodes = []
        self.scratch_tree = {}
        self.next_val_tree = {}
        self.input_block = {}
        self.sec_val = None
        self.in_val = None

    
    def get_all_targets(self,json_data):
        if isinstance(json_data,dict) and bool(json_data):
            return json_data["targets"] if 'targets' in json_data.keys() else {}
        
    
    def get_all_blocks_vals(self,blocks_values):
        targ = self.get_all_targets(blocks_values)
        return {'blocks':each_block['blocks'] for each_block in targ if isinstance(each_block,dict) and 'blocks' in each_block.keys()}
    
    def get_only_blocks(self,block_targ):
        if block_targ == None or block_targ == {}:
            return {}
        all_blocks =  self.get_all_blocks_vals(block_targ)
        return all_blocks['blocks']
    
    def get_any_block_by_id(self,blocks_values,key):
        if key == None or key == '' or blocks_values == None or blocks_values == {} or blocks_values['blocks'] == None or blocks_values['blocks'] == {} or blocks_values['blocks'][key] == None or blocks_values['blocks'][key] == {}:
            return {}
        return blocks_values['blocks'][key]

    def get_opcode_from_id(self,block_values,block_id):
        if block_id == None or block_id == '':
            return ''
        if isinstance(block_values,dict) and bool(block_values):
            return block_values['blocks'][block_id]['opcode'] if block_values['blocks'][block_id]['opcode'] != None else ''
        
    def return_all_opcodes(self,blocks_values):
        return [v2['opcode'] for k,v in blocks_values.items() for v2 in v.values() if isinstance(v,dict) and bool(v) and isinstance(v2,dict) and bool(v2) and 'opcode' in v2.keys()]

    def get_parent_opcode(self,blocks_values):
        if blocks_values == None or blocks_values == {}:
            return ''
        par = [v2['opcode'] for k,v in blocks_values.items() for v2 in v.values() if isinstance(v,dict) and bool(v) and isinstance(v2,dict) and bool(v2) and 'opcode' in v2.keys() and 'parent' in v2.keys() and v2["parent"] == None]
        return par[0] if len(par) == 1 else par
         

    def create_top_tree(self,block_values,next_values):
        if block_values == None or block_values == {}:
            return {}
        par_opcode = self.get_parent_opcode(block_values)
        if isinstance(par_opcode,list):
            for each_par in par_opcode:
                self.scratch_tree[each_par] = next_values
        else:
            self.scratch_tree[par_opcode] = next_values

            
        return self.scratch_tree  

    
    
    def read_input_values_by_id(self,blocks_values,id):
        if id == None or id == '' or blocks_values == None or blocks_values == {}:
            return {}
        return blocks_values['blocks'][id]['inputs'] if 'inputs' in blocks_values['blocks'][id].keys() else {}
    
    def check_dict_depth(self,dict_val,depth=1):
        if not isinstance(dict_val,dict) or not bool(dict_val):
            return depth
        return max(self.check_dict_depth(v,depth+1) for k,v in dict_val.items())

    
    def flatten_input_values(self,blocks_values,id):
        if id == None or id == '' or blocks_values == None or blocks_values == {}:
            return {}
        input_block = self.read_input_values_by_id(blocks_values,id)
        print(input_block)
        if input_block == None or input_block == {}:
            return {}
        if isinstance(input_block,dict) and bool(input_block):
                for k,v in input_block.items():
                    
                    if isinstance(v,list) and len(v) > 0:
                        if isinstance(v[1],list) and len(v[1]) > 0 and isinstance(v[1][1],str) and not isinstance(v[1],str):
                            self.input_block = {k:v[1][1]} if v[1][1] != '' or v[1][1] != None else {}
                                
                        elif isinstance(v[1],str) and len(v[1]) > 0 and not isinstance(v[1],list):
                            opcode = self.get_opcode_from_id(blocks_values,v[1])
                            block_by_id = self.get_any_block_by_id(blocks_values,v[1])
                            self.input_block = {k:{opcode:self.flatten_input_values(block_by_id,v[1])}}
                            
                for k2,v2 in input_block.items():
                    if k2 not in self.input_block.keys(): 
                        if isinstance(v2,list) and len(v2) > 0:
                            if isinstance(v2[1],str) and not isinstance(v2[1],list) :
                                opcode = self.get_opcode_from_id(blocks_values,v2[1])
                                print(opcode)
                                if opcode != None or opcode != '':
                                    val_flat = self.flatten_input_values(blocks_values,v2[1])
                                    
                                    if isinstance(val_flat,dict):
                                        self.sec_val = {opcode: val_flat} if self.check_dict_depth(val_flat) != 2 else {opcode:{ks:vs for ks,vs in val_flat.items()}}
                                        self.input_block = {k2:self.sec_val}
                                else:
                                    self.input_block = {k2:v2[1]}
                            elif not isinstance(v2[1],str) and isinstance(v2[1],list) and len(v2[1]) > 0 and isinstance(v2[1][1],str) and v2[1][1] != '' or v2[1][1] != None:
                                self.sec_val = v2[1][1]
                                self.input_block.update({k2:self.sec_val})

    def read_input_values(self,blocks_values,input_block):
        if input_block == None or input_block == {}:
            return {}
        if isinstance(input_block,dict) and bool(input_block):
            for k,v in input_block.items():
                    #self.input_block[k] = {}
                    if isinstance(v,list) and len(v) > 0:
                        if isinstance(v[1],list) and len(v[1]) > 0  and not isinstance(v[1],str):
                            for val in v:
                                if isinstance(val,list)  and len(val) > 0:
                                    for each_val in val:
                                        if isinstance(each_val,str):
                                            self.input_block = {k:each_val} if each_val != '' or each_val != None else {}

                                if isinstance(val,str):
                                    opcode = self.get_opcode_from_id(blocks_values,val)
                                    input_block2 = self.read_input_values_by_id(blocks_values,val)
                                    self.input_block = {k:{opcode:self.read_input_values(blocks_values,input_block2)}}
            
            for k2,v2 in input_block.items():
                if k2 not in self.input_block.keys():
                    if isinstance(v2,list) and len(v2) > 0:
                        for each_val in v2:
                            if isinstance(each_val,str):
                                opcode = self.get_opcode_from_id(blocks_values,each_val)
                                inp_blo = self.read_input_values_by_id(blocks_values,each_val)

                                if inp_blo == None or inp_blo == {} and opcode != None or opcode != '' and isinstance(opcode,str) and isinstance(inp_blo,dict) and bool(inp_blo):
                                    self.input_block = {k2:{opcode:self.read_input_values(blocks_values,inp_blo) if self.read_input_values(blocks_values,inp_blo) != {} else {}}}
                                    
                            
                            elif isinstance(each_val,list) and len(each_val) > 0:
                                for each_val2 in each_val:
                                    if isinstance(each_val2,str) and each_val2 != '' or each_val2 != None:
                                        self.sec_val = each_val2
                                        
                                        self.input_block.update({k2:self.sec_val})
                
                '''    
            
                                if inp_blo != None or inp_blo != {} and isinstance(inp_blo,dict) and bool(inp_blo):
                                    for k3,v3 in inp_blo.items():
                                        if isinstance(v3[1],list) and len(v3[1]) > 0: 
                                            if isinstance(v3[1][1],str):
                                                print(v3)
                                                val_flat = self.read_input_values(blocks_values,inp_blo)
                                            
                                                self.input_block[k2] = {k3:v3[1][1]} if v3[1][1] != '' or v3[1][1] != None else {}
                                            else:

                                                val_flat = self.read_input_values(blocks_values,inp_blo)
     
                                                self.sec_val = {opcode: val_flat} 
                                                self.input_block[k2] = {self.sec_val}
                            
                                '''
                            
            
                        
        return self.input_block

 
        
    def create_next_values(self,blocks_values):
        if blocks_values == None or blocks_values == {}:
            return {}
        return {self.get_opcode_from_id(blocks_values,v):self.read_input_values(blocks_values,self.read_input_values_by_id(blocks_values,v)) for v in self.get_all_next_id(blocks_values)}      

    def get_all_next_id(self,blocks_values):
        if blocks_values == None or blocks_values == {}:
            return {}
        return [v2["next"] for v in blocks_values.values() for k2,v2 in v.items() if isinstance(v,dict) and bool(v) and isinstance(v2,dict) and bool(v2) and 'next' in v2.keys() and v2["next"] != None]
    
    def read_files(self, parsed_file):
        self.parsed_value = self.sb3class.unpack_sb3(parsed_file)
        self.blocs_json = json.loads(self.parsed_value)
        
        

        #block values
        all_blocks_value = self.get_all_blocks_vals(self.blocs_json)
        
        #only blocks
        #only_blocks = self.get_only_blocks(self.blocs_json)
        #print(only_blocks)

        #get all opcodes
        #all_opcodes = self.return_all_opcodes(all_blocks_value)
   

        #create next values
        next_val = self.create_next_values(all_blocks_value)
        print(next_val)

        top_tree = self.create_top_tree(all_blocks_value,next_val)
        file_name = os.path.basename(parsed_file).split('/')[-1].split('.sb3')[0]

        with open(f"files/{file_name}_tree2.json","w") as tree_file:
            json.dump(top_tree,tree_file,indent=4)
        #print(top_tree)


scratch_parser_inst = scratch_parser()
scratch_parser_inst.read_files("files/test2.sb3")

    
