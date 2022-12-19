import ast


class JumpBreak:
    def __str__(self):
        return "Break()"

    def to_py_ast(self):
        return ast.Break()
