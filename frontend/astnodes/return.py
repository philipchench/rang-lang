class Return:
    def __init__(self, exp):
        self.exp = exp

    def __str__(self):
        return "Return( \n\t\t" + str(self.exp) + ")"
