import ast


class JumpPass:
    def __str__(self):
        return "Continue()"

    def to_py_ast(self):
        node = ast.Pass()
        return node
