class Node:
    def __init__(self, value, children=None):
        self.value = value
        if children:
            self.children=children
        else:
            self.children = []
            
    def set(self, children):
        self.children = children

    def indent_tree(self, level=0):
        print('\t' * level + str(self.value))
        for child in self.children:
            if child is not None:
                try:
                    child.indent_tree(level+1)
                except:
                    print(self.value)
                    print(child)

    def _preorder(self, node):
        if node is None:
            return
        self.preorderList.append(node.value)
        for child in node.children:
            self._preorder(child)

    def preorder(self):
        self.preorderList=[]
        self._preorder(self)
        return self.preorderList