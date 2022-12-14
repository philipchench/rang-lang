import sys
from frontend.token import Token


class Scanner:
    def __init__(self, file):
        self.file = file
        self.curr_line = self.file.readline()
        self.char_index = -1
        self.line_idx = 0

    def next_token(self):
        token = ""
        while True:
            new_char = self.next_char()
            if not new_char:
                return None
            if new_char == " " or new_char == "\t" or new_char == "\n":
                continue
            if new_char == "(":
                if not token:
                    token += new_char
                else:



    def next_char(self):
        if not self.curr_line:
            return None  # EOF
        self.char_index += 1
        if self.char_index < len(self.curr_line):
            return self.curr_line[self.char_index]  # base case
        else:
            self.curr_line = self.file.readline()
            self.line_idx += 1
            self.char_index = -1  # pretend we are still on "previous" character
            if not self.curr_line:
                return None  # EOF
            return self.next_char()  # recurse
