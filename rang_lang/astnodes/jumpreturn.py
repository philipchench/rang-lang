import ast


class JumpReturn:
    def __init__(self, exp):
        self.exp = exp

    def __str__(self):
        return "Return( \n\t\t" + str(self.exp) + ")"

    def to_py_ast(self):
        if not self.exp:
            node = ast.Return(None)
        else:
            node = ast.Return(self.exp.to_py_ast())
        node.lineno = 0
        node.col_offset = 0
        return node
