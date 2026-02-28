class ASTNode:
    def __init__(self, symbol, value=None, parent = None):
        self.symbol = symbol
        self.value = value
        self.children = []
        self.parent = parent
    
    def add_child(self, node):
        self.children.append(node)
        node.parent = self
    
    #debugging
    def to_string(self, indent=0):
        val_str = f": {self.value}" if self.value else ""
        s = "  " * indent + self.symbol + val_str + "\n"
        for child in self.children:
            s += child.to_string(indent + 1)
        return s

class AST:
    def __init__(self, start_symbol):
        self.root = ASTNode(start_symbol)
        # stack shows current path in tree
        self.stack = [self.root] # to handle insertion

    def insert_non_terminal(self, symbol):
        #has childeren, insert at last index [-1]
        node = ASTNode(symbol, parent=self.stack[-1])
        self.stack[-1].add_child(node) # add to top of stack
        self.stack.append(node)

    def close_non_terminal(self):
        if len(self.stack) > 1:
            self.stack.pop()

    def insert_terminal(self, symbol, value):
        # no children
        node = ASTNode(symbol, value=value, parent=self.stack[-1])
        self.stack[-1].add_child(node) # add to top of stack
        # dont add to stack

    # debugging
    def to_string(self):
        return self.root.to_string()