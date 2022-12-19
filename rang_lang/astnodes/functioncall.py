import ast
import sys

from rang_lang.astnodes.var import Var


class FunctionCall:
    def __init__(self, name: Var, exp_list: []):
        self.name = name
        self.exp_list = exp_list

    def __str__(self):
        res = "FunctionCall(Name = " + str(self.name) + ",\n\tArguments:\n"
        for exp in self.exp_list:
            res += "\t\t" + str(exp) + ",\n"
        return res + ")"

    def to_py_ast(self):
        # built-in floor()
        if self.name == "floor":
            if len(self.exp_list) != 1:
                sys.stderr.write("Bad argument length for floor() function.")
                sys.exit(1)
            return ast.Call(func=ast.Name(id='int', ctx=ast.Load()),
                            args=[ast.BinOp(left=self.exp_list[0].to_py_ast(), op=ast.FloorDiv(),
                                            right=ast.Constant(value=1))])
        # built-in power
        elif self.name == "power":
            if len(self.exp_list) != 2:
                sys.stderr.write("Bad argument length for floor() function.")
                sys.exit(1)
            return ast.BinOp(left=self.exp_list[0].to_py_ast(), op=ast.Pow(), right=self.exp_list[1].to_py_ast())
        elif self.name == "out":
            return ast.Call(func=ast.Name(id='print', ctx=ast.Load()), args=[exp.to_py_ast() for exp in self.exp_list])
        return ast.Call(func=ast.Name(id=self.name, ctx=ast.Load()), args=[exp.to_py_ast() for exp in self.exp_list])
