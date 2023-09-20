class TreeClasser:
    
    def __init__(self,class_root_name):
        self.root_name = class_root_name
        self.children  = []
        self.tree_cont = None


    def add_child(self,node):
        
        self.children.append(node)
        #print(self.children)
        #return self.children


    def setup_tree(self,children):
        
        if isinstance(children,list) and len(children) > 0:
            for each_child in children:
                print(each_child)

        
            




