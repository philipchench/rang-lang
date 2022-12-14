from frontend.scanner import Scanner


class Parser:
    def __init__(self, scanner: Scanner):
        self.scanner = scanner

    def debug_scanner(self):
        token = self.scanner.next_token()
        while token:
            print(token)
            token = self.scanner.next_token()