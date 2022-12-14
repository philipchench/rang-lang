class Token:
    def __init__(self, POS, lexeme, line_idx):
        self.POS = POS
        self.lexeme = lexeme
        self.line_idx = line_idx

    def __str__(self):
        return "< " + str(self.POS) + ", \"" + str(self.lexeme) + "\" >"
