from frontend.astnodes.exp import Exp


class Program:
    def __init__(self):
        self.statements = []

    def add_statement(self, statement: Exp):
        self.statements.append(statement)

    def get_statements(self):
        return self.statements

    def __str__(self):
        res = "Rang Program — " + str(len(self.statements)) + " statements: \n\n"
        for statement in self.statements:
            res += str(statement) + "\n"
        return res

