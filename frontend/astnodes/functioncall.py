class FunctionCall:
    def __init__(self, name: str, exp_list: []):
        self.name = name
        self.exp_list = exp_list

    def __str__(self):
        res = "Function Call:\nName = " + self.name + "\nArguments:\n"
        for exp in self.exp_list:
            res += str(exp) + "\n"
        return res


