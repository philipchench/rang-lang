import ast
import sys

from rang_lang.parser import Parser
from rang_lang.scanner import Scanner
from rang_lang.transpiler import Transpiler


def run_help():
    print("Command Syntax:")
    print("\t\t./rangc [flags] filename")
    print("\nRequired arguments:")
    print("\t\tfilename is the pathname (absolute or relative) to the input file.")
    print("\nOptional flags:")
    print("\t\t-h\t\tprints this message")
    print("\nAt most one of the following three flags:")
    print("\t\t-s\t\tis the standard compiler")


p = False
py = False

if not len(sys.argv[1:]):
    print("No command line arguments specified.")
    sys.exit(1)

try:
    arg = sys.argv[1]
    if arg == "-h":
        run_help()
        sys.exit()
    elif arg == "-p":
        p = True
    elif arg == "-py":
        py = True
    path = sys.argv[2]

except:
    sys.stderr.write("Bad argument(s).")
    sys.exit(1)

try:
    f = open(path, 'r')
except IOError:
    sys.stderr.write("ERROR: Cannot read file")
    sys.exit(1)

scanner = Scanner(f)
parser = Parser(scanner)

if p:
    parser.parse()
    # parser.debug_scanner()
    transpiler = Transpiler(parser.tree)
    tree = transpiler.build_py_ast()
    print(ast.dump(tree, indent=4))

elif py:
    parser.parse()
    transpiler = Transpiler(parser.tree)
    tree = transpiler.build_py_ast()
    exec(compile(tree, filename="<ast>", mode="exec"))

sys.exit()

