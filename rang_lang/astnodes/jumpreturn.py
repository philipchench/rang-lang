import ast


class JumpReturn:
    def __init__(self, exp):
        self.exp = exp

    def __str__(self):
        return "Return( \n\t\t" + str(self.exp) + ")"

    def to_py_ast(self):
        if not self.exp:
            return ast.Return(None)
        return ast.Return(self.exp.to_py_ast())
