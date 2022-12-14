from frontend.astnodes.exp import Exp


class BinOp:
    def __init__(self, operator: str, exp1: Exp, exp2: Exp):
        self.operator = operator
        self.exp1 = exp1
        self.exp2 = exp2

    def __str__(self):
        res = "Binary Operator: \nOperator = " + self.operator + \
              ", expression 1 = " + str(self.exp1) + ", expression 2 = " + str(self.exp2)
        return res
