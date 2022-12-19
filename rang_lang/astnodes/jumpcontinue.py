import ast


class JumpContinue:
    def __str__(self):
        return "Continue()"

    def to_py_ast(self):
        node = ast.Continue()
        return node
