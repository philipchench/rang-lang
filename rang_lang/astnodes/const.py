import ast


class Const:
    def __init__(self, value, num_type):
        self.value = value
        self.num_type = num_type  # use Utils.POS?

    def __str__(self):
        return self.value

    def to_py_ast(self):
        return ast.Constant(self.value)
