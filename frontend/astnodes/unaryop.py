from frontend.astnodes.exp import Exp


class UnaryOp:
    def __init__(self, operator: str, exp: Exp):
        self.operator = operator
        self.exp = exp

    def __str__(self):
        return "UnaryOp(Operator = " + self.operator + ", expression = " + str(self.exp) + ")"