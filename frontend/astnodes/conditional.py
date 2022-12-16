class Conditional:
    def __init__(self, exp, if_list, else_list=[]):
        self.exp = exp
        self.if_list = if_list
        self.else_list = else_list

    def __str__(self):
        res = "Conditional( \n\t\tIf condition = " + str(self.exp) + ", \n\t\t If block = "
        for statement in self.if_list:
            res += "\n\t\t" + statement
        if self.else_list:
            res += ", \n\t\tElse block = "
            for statement in self.else_list:
                res += "\n\t\t" + statement
        return res
