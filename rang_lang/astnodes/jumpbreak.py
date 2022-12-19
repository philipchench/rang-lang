import ast


class JumpBreak:
    def __str__(self):
        return "Break()"

    def to_py_ast(self):
        node = ast.Break()
        node.lineno = 0
        node.col_offset = 0
        return node
