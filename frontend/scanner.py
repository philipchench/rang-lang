import sys
from frontend.token import Token
from collections import deque


class Scanner:
    def __init__(self, file):
        self.tokens = deque()
        self.file = file
        self.curr_line = None
        self.index = None
        self.line_idx = 0

    def next_token(self):
        if self.tokens:
            return self.tokens.popleft()
        else:
            while not self.tokens:
                self.curr_line = self.file.readline()
                self.line_idx += 1
                if not self.curr_line:
                    return None
                else:
                    self.scan_next_line(self.curr_line)
            return self.tokens.popleft()

    def scan_next_line(self, line):
        pass