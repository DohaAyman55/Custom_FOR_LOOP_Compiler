class Scope:
    def __init__(self, parent=None):
        self.symbols = {} 
        self.parent = parent

    # add symbols to the scope
    def insert(self, name, symbol_info):
        if name in self.symbols:
            return False
        self.symbols[name] = symbol_info
        return True

    # search for symbol in scope and all parent scopes
    def lookup(self, name):
        if name in self.symbols:
            return self.symbols[name] # return symbol info
        if self.parent:
            return self.parent.lookup(name)
        return None

class SymbolTable:
    def __init__(self):
        self.current_scope = Scope()  # Global scope

    # add new scope
    def enter_scope(self):
        self.current_scope = Scope(parent=self.current_scope)

    # exit current scope, go to its parent
    def exit_scope(self):
        if self.current_scope.parent:
            self.current_scope = self.current_scope.parent

    #adding a new identifier to the current scope.
    def insert(self, name, type=None, value=None):
        symbol_info = {
            "type": type,
            "value": value,
        }
        return self.current_scope.insert(name, symbol_info)  #return bool
    
    # search in all scopes
    def lookup(self, name):
        return self.current_scope.lookup(name)
    
    def lookup_current_scope(self, name):
        return self.current_scope.symbols.get(name)
    
    #debugging
    def toString(self):
        print("\n=== DEBUG: Symbol Table (Scope Chain) ===")
        scope = self.current_scope
        level = 0

        while scope:
            print(f"\nScope Level {level}")
            print(f"  Scope ID: {id(scope)}")
            print(f"  Parent ID: {id(scope.parent) if scope.parent else 'None'}")

            if scope.symbols:
                print("  Symbols:")
                for name, info in scope.symbols.items():
                    print(f"    {name} -> type: {info.get('type')}, value: {info.get('value')}")
            else:
                print("  Symbols: (empty)")

            scope = scope.parent
            level += 1

        if self.current_scope.parent is None:
            print("\nCurrent scope IS global scope")
        else:
            print("\nCurrent scope is NOT global")
