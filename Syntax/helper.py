from cfg import cfg
from first_follow_sets import FIRST, FOLLOW

# current symbol = top of stack
def pick_rule(current_symbol, token):
    #get relevant rules
    production_rules = cfg[current_symbol] 

    for rule in production_rules:
        if not rule:  # epsilon production
             # Only pick epsilon if token is in FOLLOW(current_symbol)
            if token in FOLLOW[current_symbol]:
                return rule
            else:
                continue # ro7 3al rule el ba3do
            
        first_symbol = rule[0]

        # If first symbol is terminal and matches token
        if first_symbol == token:
            return rule
        
        # If first symbol is a non-terminal and token in FIRST(first_symbol)
        if first_symbol in FIRST and token in FIRST[first_symbol]:
            return rule
    return None # not in cfg aslan