import ast

from rang_lang.astnodes.exp import Exp

op_dict = {
    "&&": ast.And(),
    "||": ast.Or()
}


class BoolOp:
    def __init__(self, operator: str, exp1: Exp, exp2: Exp):
        self.operator = operator
        self.exp1 = exp1
        self.exp2 = exp2

    def __str__(self):
        res = "BinOp(Operator = \n\t\t" + self.operator + \
              ", expression 1 = \n\t\t" + str(self.exp1) + ", expression 2 = \n\t\t" + str(self.exp2) + ")"
        return res

    def to_py_ast(self):
        node = ast.BoolOp(op=op_dict[self.operator], values=[self.exp1.to_py_ast(), self.exp2.to_py_ast()])
        node.lineno = 0
        node.col_offset = 0
        return node
