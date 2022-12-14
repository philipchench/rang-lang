from frontend.astnodes.var import Var


class FunctionCall:
    def __init__(self, name: Var, exp_list: []):
        self.name = name
        self.exp_list = exp_list

    def __str__(self):
        res = "FunctionCall(Name = " + str(self.name) + ",\n\tArguments:\n"
        for exp in self.exp_list:
            res += "\t\t" + str(exp) + ",\n"
        return res + ")"


