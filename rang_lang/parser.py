import sys

from rang_lang.astnodes.assign import Assign
from rang_lang.astnodes.binop import BinOp
from rang_lang.astnodes.conditional import Conditional
from rang_lang.astnodes.const import Const
from rang_lang.astnodes.exp import Exp
from rang_lang.astnodes.function import Function
from rang_lang.astnodes.functioncall import FunctionCall
from rang_lang.astnodes.iterwhile import IterWhile
from rang_lang.astnodes.jumpbreak import JumpBreak
from rang_lang.astnodes.jumpcontinue import JumpContinue
from rang_lang.astnodes.jumpreturn import JumpReturn
from rang_lang.astnodes.program import Program
from rang_lang.astnodes.unaryop import UnaryOp
from rang_lang.astnodes.var import Var
from rang_lang.scanner import Scanner
from rang_lang.token import Token
from rang_lang.utils import Utils


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
        while self.curr_token.POS != Utils.EOF:
            print(self.curr_token)
            self.next_token()

    def parse(self):
        self.scan()
        while self.curr_token.POS != Utils.EOF:
            # print("tree: ")
            # self.print_tree()
            self.tree.add_statement(self.parse_statement())

    def parse_statement(self):
        # try assignment
        first = self.curr_token
        # while loop
        if first.POS == Utils.WHILE:
            self.next_token()
            return self.parse_while()
        # conditional
        elif first.POS == Utils.IF:
            self.next_token()
            return self.parse_conditional()
        elif first.POS == Utils.RETURN:
            self.next_token()
            # null return
            if self.curr_token.POS == Utils.SEMICOLON:
                self.next_token()
                return JumpReturn(None)
            exp = self.parse_exp()
            if self.curr_token.POS != Utils.SEMICOLON:
                self.parse_error("Missing semicolon.")
            self.next_token()
            return JumpReturn(exp)
        elif first.POS == Utils.CONTINUE:
            self.next_token()
            if self.curr_token.POS != Utils.SEMICOLON:
                self.parse_error("Missing semicolon.")
            self.next_token()
            return JumpContinue()
        elif first.POS == Utils.BREAK:
            self.next_token()
            if self.curr_token.POS != Utils.SEMICOLON:
                self.parse_error("Missing semicolon.")
            self.next_token()
            return JumpBreak()
        self.next_token()
        if self.curr_token.POS == Utils.ASSIGN:
            # assignment
            if first.POS == Utils.ID:
                self.next_token()
                # parse function
                if self.curr_token.POS == Utils.FUNC:
                    self.next_token()
                    func = self.parse_func(first.lexeme)
                    return func
                exp = self.parse_exp()
                expression = Exp(Assign(Var(first.lexeme, "store"), exp))
                # for now, assignment must end with semicolon
                if self.curr_token.POS != Utils.SEMICOLON:
                    self.parse_error("Missing semicolon.")
                self.next_token()
                return expression
            # e.g. 2 = 4, cannot assign expression to non-variable
            else:
                self.parse_error("Cannot assign expression to non-variable.")

        # try expression
        self.prev_token()
        expression = self.parse_exp()
        # for now, statement must end with semicolon
        if self.curr_token.POS != Utils.SEMICOLON:
            self.parse_error("Missing semicolon.")
        self.next_token()
        return expression

    def parse_exp(self):
        # need to deal with assignment (variable and expression) or just expression
        # for now, parse_exp deals directly with logical-or-exp

        term = self.parse_and_exp()
        while self.curr_token.POS == Utils.AND:
            op = self.curr_token.lexeme
            self.next_token()
            term2 = self.parse_and_exp()
            term = BinOp(op, term, term2)
        # at this point, term might be an add_exp, not simply a term
        return Exp(term)  # encapsulate within Exp()

    def parse_and_exp(self):
        term = self.parse_equality()
        while self.curr_token.POS == Utils.OR:
            op = self.curr_token.lexeme
            self.next_token()
            term2 = self.parse_equality()
            term = BinOp(op, term, term2)
        return term

    def parse_equality(self):
        term = self.parse_relational()
        while self.curr_token.POS == Utils.EQUALITY:
            op = self.curr_token.lexeme
            self.next_token()
            term2 = self.parse_relational()
            term = BinOp(op, term, term2)
        return term

    def parse_relational(self):
        term = self.parse_additive()
        while self.curr_token.POS == Utils.COMPARISON:
            op = self.curr_token.lexeme
            self.next_token()
            term2 = self.parse_additive()
            term = BinOp(op, term, term2)
        return term

    def parse_additive(self):
        term = self.parse_term()
        while self.curr_token.POS == Utils.ADDOP:
            op = self.curr_token.lexeme
            self.next_token()
            term2 = self.parse_term()
            term = BinOp(op, term, term2)
        return term

    def parse_term(self):
        factor = self.parse_factor()
        while self.curr_token.POS == Utils.MULTOP:
            op = self.curr_token.lexeme
            self.next_token()
            factor2 = self.parse_factor()
            factor = BinOp(op, factor, factor2)
        return factor

    def parse_factor(self):
        if self.curr_token.POS == Utils.OPEN_PAREN:
            self.next_token()
            exp = self.parse_exp()
            if self.curr_token.POS != Utils.CLOSE_PAREN:
                self.parse_error("Missing close parenthesis for expression/factor.")
            self.next_token()
            return exp
        # check if unary (negative sign)
        elif self.curr_token.lexeme == "-":
            self.next_token()
            factor = self.parse_factor()
            op = UnaryOp("-", factor)
            return op
        # check if unary (based on POS)
        elif self.curr_token.POS == Utils.UNARY:
            lexeme = self.curr_token.lexeme
            self.next_token()
            factor = self.parse_factor()
            op = UnaryOp(lexeme, factor)
            return op
        # check number
        elif self.curr_token.POS == Utils.INT or self.curr_token.POS == Utils.FLOAT:
            op = Const(self.curr_token.lexeme, self.curr_token.POS)
            self.next_token()
            return op
        elif self.curr_token.POS == Utils.ID:
            name = self.curr_token.lexeme
            self.next_token()
            # check if function
            if self.curr_token.POS == Utils.OPEN_PAREN:
                self.next_token()
                return FunctionCall(name, self.parse_func_args())
            # just regular ol' variable
            op = Var(name, "load")
            return op
        else:
            self.parse_error("Bad token for factor.")

    def parse_func_args(self):
        arguments = []
        # VERY DANGEROUS!! Must check for EOF if there's no close parenthesis at all
        while self.curr_token.POS != Utils.CLOSE_PAREN:
            if self.curr_token.POS == Utils.EOF:
                self.parse_error("Missing close parenthesis for function call.")
            exp = self.parse_exp()
            arguments.append(exp)
            if self.curr_token.POS == Utils.COMMA:
                self.next_token()
        self.next_token()
        return arguments

    def parse_func(self, name):
        arguments = []
        if self.curr_token.POS != Utils.OPEN_PAREN:
            self.parse_error("Missing open parenthesis for function.")
        self.next_token()
        # VERY DANGEROUS!! Must check for EOF if there's no close parenthesis at all
        while self.curr_token.POS != Utils.CLOSE_PAREN:
            if self.curr_token.POS == Utils.EOF:
                self.parse_error("Missing close parenthesis for function.")
            arguments.append(self.curr_token.lexeme)
            self.next_token()
            if self.curr_token.POS == Utils.COMMA:
                self.next_token()
        self.next_token()
        statements = self.parse_block()
        return Function(name, arguments, statements)

    def parse_while(self):
        if self.curr_token.POS != Utils.OPEN_PAREN:
            self.parse_error("Missing open parenthesis for while loop.")
        self.next_token()
        # condition is an expression
        exp = self.parse_exp()
        if self.curr_token.POS != Utils.CLOSE_PAREN:
            self.parse_error("Missing close parenthesis for while loop.")
        self.next_token()
        statements = self.parse_block()
        return IterWhile(exp, statements)

    def parse_conditional(self):
        if self.curr_token.POS != Utils.OPEN_PAREN:
            self.parse_error("Missing open parenthesis for if condition.")
        self.next_token()
        # condition is an expression
        exp = self.parse_exp()
        if self.curr_token.POS != Utils.CLOSE_PAREN:
            self.parse_error("Missing close parenthesis for if condition.")
        self.next_token()
        if_list = self.parse_block()
        if self.curr_token.POS == Utils.ELSE:
            self.next_token()
            else_list = self.parse_block()
            return Conditional(exp, if_list, else_list)
        return Conditional(exp, if_list)

    def parse_block(self):
        statements = []
        # start of block
        if self.curr_token.POS != Utils.OPEN_BRACKET:
            self.parse_error("Missing open bracket for block.")
        self.next_token()
        while self.curr_token.POS != Utils.CLOSE_BRACKET:
            if self.curr_token.POS == Utils.EOF:
                self.parse_error("Missing close bracket for block.")
            statement = self.parse_statement()
            statements.append(statement)
            if self.curr_token.POS == Utils.COMMA:
                self.next_token()
        self.next_token()
        if self.curr_token.POS == Utils.SEMICOLON:
            self.next_token()
        return statements

    def print_tree(self):
        print(self.tree)

    def parse_error(self, message=None):
        sys.stderr.write("Line " + str(self.curr_token.line_idx) + ": " + str(self.curr_token) + " caused parsing "
                                                                                                 "error.")
        if message:
            sys.stderr.write("\n" + message)
        sys.exit(1)
