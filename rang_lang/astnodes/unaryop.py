import ast
import sys

from rang_lang.astnodes.exp import Exp


class UnaryOp:
    def __init__(self, operator: str, exp: Exp):
        self.operator = operator
        self.exp = exp

    def __str__(self):
        return "UnaryOp(Operator = \n\t\t" + self.operator + ", expression = \n\t\t" + str(self.exp) + ")"

    def to_py_ast(self):
        if self.operator == "-":
            op = ast.USub()
        elif self.operator == "!":
            op = ast.Not()
        else:
            sys.stderr.write("Bad operator for UnaryOp() node: " + self.operator)
            sys.exit(1)
        node = ast.UnaryOp(op=op, operand=self.exp.to_py_ast())
        node.lineno = 0
        node.col_offset = 0
        return node
