import sys
from frontend.token import Token
from frontend.utils import Utils


class Scanner:
    def __init__(self, file):
        self.file = file
        self.curr_line = self.file.readline()
        self.char_index = -1
        self.line_idx = 0
        self.tokens = []

    def scan(self):
        curr_token = self.next_token()
        while curr_token:
            self.tokens.append(curr_token)
            curr_token = self.next_token()
        self.tokens.append(Token(Utils.EOF, "", self.line_idx))

    def next_token(self):
        token = ""
        new_char = self.next_char()
        if not new_char:
            return None
        while new_char == " " or new_char == "\t" or new_char == "\n":
            new_char = self.next_char()
        if new_char == "{":
            token += new_char
            return Token(Utils.OPEN_BRACKET, token, self.line_idx)
        elif new_char == "}":
            token += new_char
            return Token(Utils.CLOSE_BRACKET, token, self.line_idx)
        elif new_char == "(":
            token += new_char
            return Token(Utils.OPEN_PAREN, token, self.line_idx)
        elif new_char == ")":
            token += new_char
            return Token(Utils.CLOSE_PAREN, token, self.line_idx)
        # =, ==
        elif new_char == "=":
            token += new_char
            new_char = self.next_char()
            if new_char == "=":
                token += new_char
                return Token(Utils.EQUALITY, token, self.line_idx)
            else:
                self.char_index -= 1  # move back if we peeked and don't need it
                return Token(Utils.ASSIGN, token, self.line_idx)
        elif new_char == "+":
            token += new_char
            return Token(Utils.ADDOP, token, self.line_idx)
        elif new_char == "-":
            token += new_char
            return Token(Utils.ADDOP, token, self.line_idx)
        elif new_char == "*":
            token += new_char
            return Token(Utils.MULTOP, token, self.line_idx)
        # /, //
        elif new_char == "/":
            token += new_char
            new_char = self.next_char()
            if new_char == "/":
                # comment
                token += new_char
                self.next_line()
                return self.next_token()
            else:
                self.char_index -= 1  # move back if we peeked and don't need it
                return Token(Utils.MULTOP, token, self.line_idx)
        elif new_char == "%":
            token += new_char
            return Token(Utils.MULTOP, token, self.line_idx)
        # !, !=
        elif new_char == "!":
            token += new_char
            new_char = self.next_char()
            if new_char == "=":
                token += new_char
                return Token(Utils.EQUALITY, token, self.line_idx)
            else:
                self.char_index -= 1  # move back if we peeked and don't need it
                return Token(Utils.UNARY, token, self.line_idx)
        # >, >=
        elif new_char == ">":
            token += new_char
            new_char = self.next_char()
            if new_char == "=":
                token += new_char
                return Token(Utils.COMPARISON, token, self.line_idx)
            else:
                self.char_index -= 1  # move back if we peeked and don't need it
                return Token(Utils.COMPARISON, token, self.line_idx)
        # <, <=
        elif new_char == "<":
            token += new_char
            new_char = self.next_char()
            if new_char == "=":
                token += new_char
                return Token(Utils.COMPARISON, token, self.line_idx)
            else:
                self.char_index -= 1  # move back if we peeked and don't need it
                return Token(Utils.COMPARISON, token, self.line_idx)
        # &&
        elif new_char == "&":
            token += new_char
            new_char = self.next_char()
            if new_char == "&":
                token += new_char
                return Token(Utils.ANDOR, token, self.line_idx)
            else:
                self.token_error(token)
        # ||
        elif new_char == "|":
            token += new_char
            new_char = self.next_char()
            if new_char == "|":
                token += new_char
                return Token(Utils.ANDOR, token, self.line_idx)
            else:
                self.token_error(token)
        elif new_char == ";":
            token += new_char
            return Token(Utils.SEMICOLON, token, self.line_idx)
        elif new_char == ",":
            token += new_char
            return Token(Utils.COMMA, token, self.line_idx)
        # identifier or number
        elif new_char.isalnum() or new_char == "_":
            is_id = new_char.isalpha()
            is_float = False
            while new_char and (new_char.isalnum() or new_char == "." or new_char == "_"):
                token += new_char
                if new_char == ".":
                    if is_float or is_id:
                        self.token_error(token)  # can't have 2 "."
                    is_float = True
                elif new_char == "_":
                    if is_float:
                        self.token_error(token)
                    is_id = True
                new_char = self.next_char()
            self.char_index -= 1
            # integer
            if not is_id and not is_float:
                return Token(Utils.INT, token, self.line_idx)
            # float
            elif not is_id:
                return Token(Utils.FLOAT, token, self.line_idx)
            # alphanumeric underscore combination string
            elif not is_float:
                # keep scanner simple, can sacrifice a bit of runtime
                if token == "while":
                    return Token(Utils.WHILE, token, self.line_idx)
                elif token == "if":
                    return Token(Utils.IF, token, self.line_idx)
                elif token == "else":
                    return Token(Utils.ELSE, token, self.line_idx)
                elif token == "continue":
                    return Token(Utils.CONTINUE, token, self.line_idx)
                elif token == "break":
                    return Token(Utils.BREAK, token, self.line_idx)
                elif token == "return":
                    return Token(Utils.RETURN, token, self.line_idx)
                elif token == "func":
                    return Token(Utils.FUNC, token, self.line_idx)
                return Token(Utils.ID, token, self.line_idx)
            else:
                self.token_error(token)  # should never happen
        # bad char
        else:
            token += new_char
            self.token_error(token)

    def next_char(self):
        if not self.curr_line:
            return None  # EOF
        self.char_index += 1
        if self.char_index < len(self.curr_line):
            return self.curr_line[self.char_index]  # base case
        else:
            self.next_line()
            return self.next_char()  # recurse

    def next_line(self):
        self.curr_line = self.file.readline()
        self.line_idx += 1
        self.char_index = -1  # pretend we are still on "previous" character

    def token_error(self, token):
        sys.stderr.write("Line " + str(self.line_idx) + ": " + token + " is not a valid input.")
        sys.exit(1)

    def print_tokens(self):
        for token in self.tokens:
            print(token)
