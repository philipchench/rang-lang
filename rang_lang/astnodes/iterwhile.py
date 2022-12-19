import ast

from rang_lang.astnodes.jumppass import JumpPass


class IterWhile:
    def __init__(self, exp, statement_list):
        self.exp = exp
        self.statement_list = statement_list

    def __str__(self):
        res = "While( \n\t\tCondition = " + str(self.exp) + ", \n\t\t Block = "
        for statement in self.statement_list:
            res += "\n\t\t" + str(statement)
        return res

    def to_py_ast(self):
        if not self.statement_list:
            self.statement_list.append(JumpPass())
        node = ast.While(test=self.exp.to_py_ast(), body=[stmt.to_py_ast() for stmt in self.statement_list], orelse=[])
        return node
