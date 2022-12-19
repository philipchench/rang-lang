class Exp:
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        return str(self.expression)

    def to_py_ast(self):
        return self.expression.to_py_ast()
