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
        # handle built-in "variables"
        # true
        if self.name == "true":
            node = ast.Constant(value=True)
        # false
        elif self.name == "false":
            node = ast.Constant(value=False)
        else:
            node = ast.Name(id=self.name, ctx=ctx)
        return node
