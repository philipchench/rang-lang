class Var:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return "Variable:\nName = " + self.name
