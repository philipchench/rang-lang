class IterWhile:
    def __init__(self, exp, statement_list):
        self.exp = exp
        self.statement_list = statement_list

    def __str__(self):
        res = "While( \n\t\tCondition = " + str(self.exp) + ", \n\t\t Block = "
        for statement in self.statement_list:
            res += "\n\t\t" + str(statement)
        return res
