from rang_lang.astnodes.exp import Exp


class Program:
    def __init__(self):
        self.statements = []

    def add_statement(self, statement: Exp):
        # NOTE TO SELF: might need to change from Exp to a new Stmt class in the future
        self.statements.append(statement)

    def get_statements(self):
        return self.statements

    def __str__(self):
        res = "Rang Program — " + str(len(self.statements)) + " statements: \n\n"
        for i in range(len(self.statements)):
            res += "Statement " + str(i) + ":\n" + str(self.statements[i]) + "\n"
        return res
