import ast


class Conditional:
    def __init__(self, exp, if_list, else_list=[]):
        self.exp = exp
        self.if_list = if_list
        self.else_list = else_list

    def __str__(self):
        res = "Conditional( \n\t\tIf condition = " + str(self.exp) + ", \n\t\t If block = "
        for statement in self.if_list:
            res += "\n\t\t" + str(statement)
        if self.else_list:
            res += ", \n\t\tElse block = "
            for statement in self.else_list:
                res += "\n\t\t" + str(statement)
        return res + ")"

    def to_py_ast(self):
        node = ast.If(test=self.exp.to_py_ast(), body=[stmt.to_py_ast() for stmt in self.if_list],
                      orelse=[stmt.to_py_ast() for stmt in self.else_list])
        node.lineno = 0
        node.col_offset = 0
        return node