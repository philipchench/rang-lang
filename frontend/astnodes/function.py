class Function:
    def __init__(self, name, args, statement_list):
        self.name = name
        self.args = args
        self.statement_list = statement_list

    def __str__(self):
        res = "Function( \n\t\tName = " + str(self.name) + ",\n\tArguments:\n"
        for arg in self.args:
            res += "\t\t" + str(arg) + ",\n"
        res += ", \n\t\t Block = "
        for statement in self.statement_list:
            res += "\n\t\t" + statement
        return res
