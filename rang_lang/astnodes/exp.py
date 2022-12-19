import ast


class Exp:
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        return str(self.expression)

    def to_py_ast(self):
        node = ast.Expr(self.expression.to_py_ast())
        node.lineno = 0
        node.col_offset = 0
        return node
