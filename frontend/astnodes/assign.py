from frontend.astnodes.exp import Exp
from frontend.astnodes.var import Var


class Assign:
    def __init__(self, var: Var, exp: Exp):
        self.var = var
        self.exp = exp

    def __str__(self):
        res = "Assign(Variable name = \n\t\t" + str(self.var) + ", assignment = \n\t\t" + str(self.exp) + ")"
        return res

