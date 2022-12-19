import ast
import sys


class Var:
    def __init__(self, name: str, mode: str):
        self.name = name
        self.mode = mode

    def __str__(self):
        return self.mode + "(" + self.name + ")"

    def to_py_ast(self):
        if self.mode == "load":
            ctx = ast.Load()
        elif self.mode == "store":
            ctx = ast.Store()
        else:
            sys.stderr.write("bad mode for Var() node: " + self.name)
            sys.exit(1)
        node = ast.Name(id=self.name, ctx=ctx)
        node.lineno = 0
        node.col_offset = 0
        return node
