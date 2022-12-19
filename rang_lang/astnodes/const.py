import ast

from rang_lang.utils import Utils


class Const:
    def __init__(self, value, num_type):
        self.value = value
        self.num_type = num_type  # use Utils.POS?

    def __str__(self):
        return self.value

    def to_py_ast(self):
        if self.num_type == Utils.INT:
            node =  ast.Constant(int(self.value))
        else:
            node = ast.Constant(float(self.value))
        node.lineno = 0
        node.col_offset = 0
        return node
