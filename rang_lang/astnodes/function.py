import ast


class Function:
    def __init__(self, name, args: str, statement_list):
        self.name = name
        self.args = args
        self.statement_list = statement_list

    def __str__(self):
        res = "Function( \n\t\tName = " + str(self.name) + ",\n\tArguments:\n"
        for arg in self.args:
            res += "\t\t" + arg + ",\n"
        res += ", \n\t\t Block = "
        for statement in self.statement_list:
            res += "\n\t\t" + str(statement)
        return res

    def to_py_ast(self):
        return ast.FunctionDef(name=self.name, args=ast.arguments(args=[ast.arg(arg=arg) for arg in self.args]),
                               body=[stmt.to_py_ast() for stmt in self.statement_list])
