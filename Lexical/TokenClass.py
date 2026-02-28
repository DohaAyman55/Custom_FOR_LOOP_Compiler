class Token:
    def __init__(self, type, value, line):
        self.value = value
        self.type = type
        self.line = line
    # self.column = column

    def print_token(self):
        print("Token:")
        print(f"  Type : {self.type}")
        print(f"  Value: {self.value}")
        print(f"  Line : {self.line}")