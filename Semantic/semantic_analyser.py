import sys
import os

#force root directory Add Syntax folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SYNTAX_DIR = os.path.join(BASE_DIR, "Syntax")
sys.path.insert(0, SYNTAX_DIR)

from Parser import ast
from semantic_helper import build_symbol_table
from SymbolTable import SymbolTable

symbol_table = SymbolTable()
build_symbol_table(ast.root, symbol_table) #recursive function
print(symbol_table.toString())