import ast

from rang_lang.astnodes.exp import Exp
from rang_lang.astnodes.var import Var


class Assign:
    def __init__(self, var: Var, exp: Exp):
        self.var = var
        self.exp = exp

    def __str__(self):
        res = "Assign(Variable name = \n\t\t" + str(self.var) + ", assignment = \n\t\t" + str(self.exp) + ")"
        return res

    def to_py_ast(self):
        node = ast.Assign(targets=[self.var.to_py_ast()], value=self.exp.to_py_ast())
        return node
