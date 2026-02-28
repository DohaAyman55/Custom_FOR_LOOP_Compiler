import sys
import os

#force root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from Lexical.Scanner import tokens
from cfg import cfg
from AST import AST
from helper import pick_rule

# for token in tokens:
#     token.print_token()

start_symbol = "PROGRAM"
stack = ["$"]
stack.append(start_symbol)
# input = tokens + ["$"]
input = [(t.type, t.value) for t in tokens] + [("$", None)]
index = 0
ast = AST(start_symbol)

while stack:
    current_token, current_token_value = input[index]
    top = stack.pop()
    # #debugging
    # print(f"\n=== Parser Step ===")
    # print(f"Parser stack top: {top}")
    # print(f"Current token: {current_token}")
    # print(f"AST stack: {[n.symbol for n in ast.stack]}")

    # at the end
    if top == "$":
        if current_token == "$":
            # print("Parsing complete!")
            # remove $ from stack
            # pop remaining _CLOSE markers if any
            while stack and stack[-1].endswith("_CLOSE"):
                stack.pop()
            break
        else:
            print(f"Unexpected token: {current_token}")
            break


    if top.endswith("_CLOSE"):
        ast.close_non_terminal()
        continue  

    elif top == current_token:
        #MATCH
        index+=1
        #add leaf to tree
        ast.insert_terminal(top, current_token_value)
    
    #searcg for relevant rule in cfg
    elif top in cfg:
        #choose a production rule
        rule = pick_rule(top, current_token)

        # only push if the rule is not empty
        if rule is not None:
            # add non-terminal to tree
            #update tree (AST)
            if not (top == start_symbol and len(ast.stack) == 1): # don't re-add the start symbol
                ast.insert_non_terminal(top)
            #mark where to end non-terminal
            stack.append(f"{top}_CLOSE") 
            for symbol in reversed(rule):
                stack.append(symbol)
        
    #if nothing similar is in production rules->
    else: 
        print(f'Unexpected Token, {top}') 
        break

if index == len(input)-1 and not stack:
    print("Parsing succeeded")
else:
    print("Parsing failed")

# debugging
# print("=== AST ===")
# print(ast.to_string())