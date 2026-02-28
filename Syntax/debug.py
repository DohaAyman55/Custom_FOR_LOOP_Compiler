import sys
import os

#force root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from Lexical.Scanner import tokens
from cfg import cfg
from AST import AST
from helper import pick_rule

start_symbol = "PROGRAM"
stack = ["$"]
stack.append(start_symbol)
# input = tokens + ["$"]
input = [(t.type, t.value) for t in tokens] + [("$", None)]
index = 0
ast = AST(start_symbol)

print("=== Parsing Start ===")
print(f"Input tokens: {[t.type for t in tokens]}")

while stack:
    current_token, current_token_value = input[index]
    top = stack.pop()
    
    # DEBUG: show stack and current token
    print(f"\nStack top: {top}")
    print(f"Current token: {current_token}")
    print(f"Remaining stack: {stack}")

    if top == "$":
        if current_token == "$":
            print("Parsing complete!")
            # remove $ from stack
            while stack and stack[-1].endswith("_CLOSE"):
                stack.pop()
            break
        else:
            print(f"Unexpected token: {current_token}")
            break

    if top.endswith("_CLOSE"):
        ast.close_non_terminal()
        print(f"Closed non-terminal: {top}")
        continue  

    elif top == current_token:
        # MATCH
        index += 1
        ast.insert_terminal(top, current_token_value)
        print(f"Matched terminal: {top}, advancing to token index {index}")
    
    elif top in cfg:
        # choose a production rule
        rule = pick_rule(top, current_token)
        print(f"Pick rule for {top} with token {current_token}: {rule}")

        # only push if the rule is not empty
        if rule is not None:
            ast.insert_non_terminal(top)
            print(f"Expanding non-terminal: {top}, pushing rule to stack: {list(reversed(rule))}")
            for symbol in reversed(rule):
                stack.append(symbol)
            # mark where to end non-terminal
            stack.append(f"{top}_CLOSE")
            print(f"Stack after expansion: {stack}")
        
    else: 
        print(f'Unexpected Token, {top}') 
        break

# Final parsing result
if index == len(input)-1 and not stack:
    print("Parsing succeeded")
else:
    print("Parsing failed")

print("=== Parsing End ===")

print("=== AST ===")
print(ast.to_string())
