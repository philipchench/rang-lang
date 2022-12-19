import ast

from rang_lang.astnodes.exp import Exp

op_dict = {
    "==": ast.Eq(),
    "!=": ast.NotEq(),
    ">": ast.Gt(),
    ">=": ast.GtE(),
    "<": ast.Lt(),
    "<=": ast.LtE(),
}


class CompareOp:
    def __init__(self, operator: str, exp1: Exp, exp2: Exp):
        self.operator = operator
        self.exp1 = exp1
        self.exp2 = exp2

    def __str__(self):
        res = "BinOp(Operator = \n\t\t" + self.operator + \
              ", expression 1 = \n\t\t" + str(self.exp1) + ", expression 2 = \n\t\t" + str(self.exp2) + ")"
        return res

    def to_py_ast(self):
        node = ast.Compare(left=self.exp1.to_py_ast(), ops=[op_dict[self.operator]], comparators=[self.exp2.to_py_ast()])
        return node
