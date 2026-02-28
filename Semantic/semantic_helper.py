# ast in-order traversal (DFS)
# if new identifier found add it to the sybmol table, 
# else check for type consistency and multiple declarations


def build_symbol_table(node, symbol_table, depth=0):

    indent = "  " * depth

    # print(f"{indent}Visiting: {node.symbol} {'(' + node.value + ')' if node.value else ''}")
    if node is None: #stopping condition (recurssion)
        return

    # add new scope
    if node.symbol in {"BLOCK", "FOR_LOOP"}: # they contain tnew scopes
        # print(f"{indent}Entering new scope")
        symbol_table.enter_scope()

    if node.symbol == "IDENTIFIER":
        name = node.value.strip()  
        
        if is_declaration(node):
            # declaration
            if not symbol_table.lookup_current_scope(name): # else reassignment
                symbol_table.insert(name, "int")
        else:
            if not symbol_table.lookup(name): #search all parent scopes
                raise Exception(f"Semantic Error: '{name}' undeclared")

    for child in node.children:
        build_symbol_table(child, symbol_table, depth+1)

    if node.symbol in {"BLOCK", "FOR_LOOP"}:
        # print(f"{indent}Exiting scope")
        symbol_table.exit_scope()


def is_declaration(node):
    parent = node.parent
    if not parent:
        return False
    
    # print(f"{node.symbol} → {parent.symbol}", end="")
    
    # if parent.parent:
    #     print(f" → {parent.parent.symbol}")
    # else:
    #     print(" → None")
    
    if parent.symbol == "ASSIGN_EXPR":
        if parent.parent and parent.parent.symbol == "INIT":
            # print(f"   Declaration found (for loop init)")
            return True

    if parent.symbol == "ASSIGN_STMT":
        # print(f"   Declaration found (assign statement)")
        return True
    
    # print(f"  Not a declaration")
    return False
