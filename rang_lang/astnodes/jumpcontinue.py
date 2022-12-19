import ast


class JumpContinue:
    def __str__(self):
        return "Continue()"

    def to_py_ast(self):
        return ast.Continue()
