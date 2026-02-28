def type_check_assignment(node, symbol_table):
    left_var = None
    right_expr = None

    for child in node.children:
        if child.symbol == "IDENTIFIER":
            left_var = child
        elif child.symbol == "EXPR":
            right_expr = child

    if not left_var or not right_expr:
        return True, ""

    var_name = left_var.value.strip()
    var_info = symbol_table.lookup(var_name)

    if not var_info:
        return False, f"Undeclared variable '{var_name}'"

    left_type = var_info.get("type")
    right_type = infer_expression_type(right_expr, symbol_table)

    if left_type != right_type:
        return False, f"Type mismatch: Cannot assign {right_type} to {left_type} variable '{var_name}'"

    return True, ""


def infer_expression_type(expr_node, symbol_table):
    """
    Determine type of an expression node (int or bool).
    Following CFG.
    """
    if expr_node is None:
        return "int"
    
    if expr_node.symbol == "NUMBER":
        return "int"
    
    if expr_node.symbol == "IDENTIFIER":
        info = symbol_table.lookup(expr_node.value.strip())
        if info:
            return info.get("type", "int")
        return "int"

    if expr_node.symbol == "EXPR":
        # EXPR → TERM EXPR_PRIME
        term_type = None
        for child in expr_node.children:
            if child.symbol == "TERM":
                term_type = infer_term_type(child, symbol_table)
            # EXPR_PRIME adds terms, always int
        return term_type or "int"

    if expr_node.symbol == "COND":
        # COND → EXPR COND_PRIME
        left_type = infer_expression_type(expr_node.children[0], symbol_table)  # EXPR
        if len(expr_node.children) > 1:
            cond_prime = expr_node.children[1]
            if cond_prime.symbol == "COND_PRIME" and cond_prime.children:
                # REL_OP EXPR → boolean
                return "bool"
        return "int"

    if expr_node.symbol == "COND_PRIME":
        # REL_OP EXPR or ε
        if expr_node.children:
            return "bool"
        return "int"

    return "int"


def infer_term_type(term_node, symbol_table):
    """Determine type of a TERM node (int only)"""
    for child in term_node.children:
        if child.symbol == "FACTOR":
            factor_type = infer_factor_type(child, symbol_table)
            if factor_type == "bool":
                raise Exception("Semantic Error: Cannot use boolean in arithmetic expression")
            return factor_type
    return "int"  # default

def infer_factor_type(factor_node, symbol_table):
    """Determine type of a FACTOR node (int or bool if standalone)"""
    for child in factor_node.children:
        if child.symbol == "NUMBER":
            return "int"
        elif child.symbol == "IDENTIFIER":
            info = symbol_table.lookup(child.value.strip())
            if not info:
                raise Exception(f"Semantic Error: '{child.value.strip()}' undeclared")
            return info.get("type", "int")
        elif child.symbol == "EXPR":
            return infer_expression_type(child, symbol_table)
    return "int"

def get_rhs_expression(identifier_node):
    """
    Find the expression being assigned to this identifier.
    Supports ASSIGN_STMT and ASSIGN_EXPR.
    """
    parent = identifier_node.parent
    if not parent:
        return None

    # Only handle assignments
    if parent.symbol in {"ASSIGN_EXPR", "ASSIGN_STMT"}:
        # Locate this identifier in children
        for i, child in enumerate(parent.children):
            if child is identifier_node:
                assign_found = False
                for j in range(i + 1, len(parent.children)):
                    next_child = parent.children[j]
                    if next_child.symbol == "ASSIGN":
                        assign_found = True
                    elif assign_found and next_child.symbol == "EXPR":
                        return next_child
                break

    return None