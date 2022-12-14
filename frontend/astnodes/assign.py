from frontend.astnodes.exp import Exp
from frontend.astnodes.var import Var


class Assign:
    def __init__(self, var: Var, exp: Exp):
        self.var = var
        self.exp = exp

    def __str__(self):
        res = "Assignment: \nVariable name = " + str(self.var) + ", assignment = " + str(self.exp)
        return res

