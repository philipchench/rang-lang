import ast


class JumpContinue:
    def __str__(self):
        return "Continue()"

    def to_py_ast(self):
        node =  ast.Continue()
        node.lineno = 0
        node.col_offset = 0
        return node
