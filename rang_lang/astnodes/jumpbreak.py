import ast


class JumpBreak:
    def __str__(self):
        return "Break()"

    def to_py_ast(self):
        node = ast.Break()
        return node
