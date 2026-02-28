cfg = {

    "PROGRAM": [
        ["STMT_LIST"]
    ],

    "STMT_LIST": [
        ["STMT", "STMT_LIST"],
        []   # ε
    ],

    "STMT": [
        ["FOR_LOOP"],
        ["ASSIGN_STMT"],
        ["INC_DEC_STMT"],
        ["BLOCK"]
    ],

    # For loop
    "FOR_LOOP": [
        ["FOR", "LEFT_PAREN", "INIT", "SEMICOLON", "COND", "SEMICOLON", "UPDATE", "RIGHT_PAREN", "STMT"]
    ],

    # Init, condition, update (no semicolons inside)
    "INIT": [
        ["ASSIGN_EXPR"]
    ],

    "COND": [
        ["EXPR", "COND_PRIME"],
        []
    ],

    "COND_PRIME": [
        ["REL_OP", "EXPR"],
        []
    ],

    "UPDATE": [
        ["IDENTIFIER", "UPDATE_PRIME"],
        []
    ],

    "UPDATE_PRIME": [
        ["ASSIGN", "EXPR"],
        ["INCREMENT"],
        ["DECREMENT"]
    ],

    # Assignment with semicolon (for normal statements)
    "ASSIGN_STMT": [
        ["IDENTIFIER", "ASSIGN", "EXPR", "SEMICOLON"]
    ],

    # Assignment without semicolon (for INIT/UPDATE in for loop)
    "ASSIGN_EXPR": [
        ["IDENTIFIER", "ASSIGN", "EXPR"]
    ],

    "INC_DEC_STMT": [
        ["IDENTIFIER", "INCREMENT", "SEMICOLON"],
        ["IDENTIFIER", "DECREMENT", "SEMICOLON"]
    ],

    # Block
    "BLOCK": [
        ["LEFT_BRACE", "STMT_LIST", "RIGHT_BRACE"]
    ],

    # Expressions (non-left-recursive)
    "EXPR": [
        ["TERM", "EXPR_PRIME"]
    ],

    "EXPR_PRIME": [
        ["ADD_OP", "TERM", "EXPR_PRIME"],
        []   # ε
    ],

    "TERM": [
        ["FACTOR", "TERM_PRIME"]
    ],

    "TERM_PRIME": [
        ["MUL_OP", "FACTOR", "TERM_PRIME"],
        []   # ε
    ],

    "ADD_OP": [
        ["PLUS"],
        ["MINUS"]
    ],

    "MUL_OP": [
        ["MULTIPLY"],
        ["DIVIDE"]
    ],

    "FACTOR": [
        ["IDENTIFIER"],
        ["NUMBER"],
        ["LEFT_PAREN", "EXPR", "RIGHT_PAREN"],
    ],

    "REL_OP": [
        ["LESS_THAN"],
        ["GREATER_THAN"],
        ["LESS_EQUAL"],
        ["GREATER_EQUAL"],
        ["EQUALS"],
        ["NOT_EQUAL"]
    ]
}
