import ast

from rang_lang.astnodes.jumppass import JumpPass


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
        args_processed = []
        for arg in self.args:
            ast_arg = ast.arg(arg=arg)
            args_processed.append(ast_arg)
        arguments = ast.arguments(posonlyargs=[], args=args_processed, kwonlyargs=[], kw_defaults=[], defaults=[])
        if not self.statement_list:
            self.statement_list.append(JumpPass())
        node = ast.FunctionDef(name=self.name, args=arguments,
                               body=[stmt.to_py_ast() for stmt in self.statement_list], decorator_list=[])
        return node
