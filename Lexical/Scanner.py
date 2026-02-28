
### Token class ###
import sys
import os

#force root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

### Dictionaries to identify character token ###
from Lexical.TokenClass import Token
from Lexical.TokenTypes import keywords, operators, delimiters

def check_token_type(buffer):
    buffer = buffer.strip()

    #skip whitspace
    if buffer == "":
        return None

    if(buffer in keywords):
        token_type = keywords[buffer]
    elif(buffer in operators):
        token_type = operators[buffer]
    elif(buffer in delimiters):
        token_type = delimiters[buffer]
    elif buffer.isidentifier():
        token_type = "IDENTIFIER"
    elif buffer.isdigit():
        token_type = "NUMBER"
    else:
        token_type = "UNKNOWN"
    return token_type

### read file ### 
### separate into suitable tokens (use a buffer + array of tokens) ###  
### identify a type for each token ###
### return a list of tokens ###

tokens = []
line_number = 0
buffer = ""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_PATH = os.path.join(BASE_DIR, "source.txt")

with open(SOURCE_PATH, "r") as file:
    lines = file.readlines()
    for line in lines:
        line_number += 1
        i = 0
        while i < len(line):
            char = line[i]

            # lama el kelma tekhlas
            if char.isspace() and buffer != "":
                token_type = check_token_type(buffer) 
                if token_type is not None: # not whitespace
                    tokens.append(Token(type=token_type, value=buffer, line=line_number))
                buffer = ""
                i+=1
                continue
            

            elif char in operators:
                if buffer != "":
                    token_type = check_token_type(buffer)
                    if token_type is not None:
                        tokens.append(Token(type=token_type, value=buffer, line=line_number))
                    buffer = ""
                

                current_char = char
                next_char = line[i+1] if i + 1 < len(line) else ''
                potential_op = current_char + next_char
                if potential_op in operators:
                    tokens.append(Token(type=operators[potential_op], value=potential_op, line=line_number))
                    i+=2 # passed 2 chars at a time
                else:
                    tokens.append(Token(type=operators[char], value=char, line=line_number))
                    i+=1 # append current char only
                    continue

            elif char in delimiters:
                if buffer != "":
                    token_type = check_token_type(buffer)
                    if token_type is not None:
                        tokens.append(Token(type=token_type, value=buffer, line=line_number))
                    buffer = ""

                tokens.append(Token(type=delimiters[char], value=char, line=line_number))
                i+=1
                continue

            else:
                buffer += char
                i+=1
        
        # check buffer after loop, tokenise remaining toekn
        if buffer != "":
            token_type = check_token_type(buffer) 
            if token_type is not None:
                tokens.append(Token(type=token_type, value=buffer, line=line_number))
            buffer = ""

### output in file ###
OUTPUT_PATH = os.path.join(os.path.dirname(BASE_DIR), "stream_of_tokens.txt")
with open(OUTPUT_PATH, "w") as outfile:
    for token in tokens:
        outfile.write(f"Line {token.line}: {token.type} ('{token.value}')\n")

        