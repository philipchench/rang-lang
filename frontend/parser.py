import sys

from frontend.astnodes.assign import Assign
from frontend.astnodes.binop import BinOp
from frontend.astnodes.const import Const
from frontend.astnodes.exp import Exp
from frontend.astnodes.functioncall import FunctionCall
from frontend.astnodes.program import Program
from frontend.astnodes.unaryop import UnaryOp
from frontend.astnodes.var import Var
from frontend.scanner import Scanner
from frontend.token import Token
from frontend.utils import Utils


class Parser:
    def __init__(self, scanner: Scanner):
        self.scanner = scanner
        self.tree = Program()
        self.curr_token = Token(None, None, 0)  # random initialization for type hinting
        self.curr_idx = 0
        self.function_set = set(["out", "floor", "exp"])

    def scan(self):
        self.scanner.scan()
        if self.scanner.tokens:
            self.curr_token = self.scanner.tokens[0]
        else:
            self.curr_token = None

    def next_token(self):
        # can be used as a void, but returns curr_token regardless
        self.curr_idx += 1
        if self.curr_idx >= len(self.scanner.tokens):
            self.curr_token = None
            return None
        self.curr_token = self.scanner.tokens[self.curr_idx]
        return self.curr_token

    def prev_token(self):
        self.curr_idx -= 1
        if self.curr_idx < 0:
            self.curr_token = None
            return None
        self.curr_token = self.scanner.tokens[self.curr_idx]
        return self.curr_token

    def debug_scanner(self):
        self.scan()
        while self.curr_token:
            print(self.curr_token)
            self.next_token()

    def parse(self):
        self.scan()
        while self.curr_token:
            # print("tree: ")
            # self.print_tree()
            self.tree.add_statement(self.parse_statement())

    def parse_statement(self):
        # for now, it's just parse expression
        expression = self.parse_exp()
        # for now, statement must end with semicolon
        if self.curr_token.POS != Utils.SEMICOLON:
            self.parse_error("Missing semicolon.")
        self.next_token()
        return expression

    def parse_exp(self):
        # need to deal with assignment (variable and expression) or just expression
        # for now, parse_exp deals directly with additive_exp

        # try assignment
        first = self.curr_token
        self.next_token()
        if self.curr_token.POS == Utils.ASSIGN:
            # assignment
            if first.POS == Utils.ID:
                self.next_token()
                exp = self.parse_exp()
                return Exp(Assign(Var(first.lexeme), exp))
            # e.g. 2 = 4, cannot assign expression to non-variable
            else:
                self.parse_error("Cannot assign expression to non-variable.")

        # try additive expression
        self.prev_token()
        term = self.parse_term()
        while self.curr_token.POS == Utils.ADDOP:
            add_op = self.curr_token.lexeme
            self.next_token()
            term2 = self.parse_term()
            term = BinOp(add_op, term, term2)
        # at this point, term might be an add_exp, not simply a term
        return Exp(term)  # encapsulate within Exp()

    def parse_term(self):
        factor = self.parse_factor()
        while self.curr_token.POS == Utils.MULTOP:
            mult_op = self.curr_token.lexeme
            self.next_token()
            factor2 = self.parse_factor()
            factor = BinOp(mult_op, factor, factor2)
        return factor

    def parse_factor(self):
        if self.curr_token.POS == Utils.OPEN_PAREN:
            self.next_token()
            exp = self.parse_exp()
            if self.curr_token.POS != Utils.CLOSE_PAREN:
                self.parse_error("Missing closing parenthesis for expression/factor.")
            self.next_token()
            return exp
        # check if unary (negative sign), NOTE TO SELF: MAKE FUNCTION IF MORE UNARY OPS IN FUTURE
        elif self.curr_token.lexeme == "-":
            self.next_token()
            factor = self.parse_factor()
            op = UnaryOp("-", factor)
            return op
        # check number
        elif self.curr_token.POS == Utils.INT or self.curr_token.POS == Utils.FLOAT:
            op = Const(self.curr_token.lexeme, self.curr_token.POS)
            self.next_token()
            return op
        elif self.curr_token.POS == Utils.ID:
            # check if function (for now: out, floor, or exp)
            if self.curr_token.lexeme in self.function_set:
                name = self.curr_token.lexeme
                self.next_token()
                return FunctionCall(name, self.parse_func_args())
            # just regular ol' variable
            op = Var(self.curr_token.lexeme)
            self.next_token()
            return op
        else:
            self.parse_error("Bad token for factor.")

    def parse_func_args(self):
        arguments = []
        if self.curr_token.POS != Utils.OPEN_PAREN:
            self.parse_error("Missing closing parenthesis for function call.")
        self.next_token()
        # VERY DANGEROUS!! Must check for EOF if there's no close parenthesis at all
        while self.curr_token.POS != Utils.CLOSE_PAREN:
            if not self.curr_token:
                self.parse_error("Missing closing parenthesis for function call.")
            exp = self.parse_exp()
            arguments.append(exp)
            if self.curr_token and self.curr_token.POS == Utils.COMMA:
                self.next_token()
        self.next_token()
        return arguments

    def print_tree(self):
        print(self.tree)

    def parse_error(self, message=None):
        sys.stderr.write("Line " + str(self.curr_token.line_idx) + ": " + str(self.curr_token) + " caused parsing "
                                                                                                 "error.")
        if message:
            sys.stderr.write("\n" + message)
        sys.exit(1)
