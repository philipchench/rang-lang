from frontend.astnodes.program import Program
from frontend.scanner import Scanner


class Parser:
    def __init__(self, scanner: Scanner):
        self.scanner = scanner
        self.tree = Program()
        self.curr_token = None

    def debug_scanner(self):
        token = self.scanner.next_token()
        while token:
            print(token)
            token = self.scanner.next_token()

    def parse(self):
        self.curr_token = self.scanner.next_token()
        while self.curr_token:
            self.tree.append(self.parse_statement())
            self.curr_token = self.scanner.next_token()

    def parse_statement(self):
        pass

    def parse_exp(self):
        pass

    def print_tree(self):
        print(self.tree)