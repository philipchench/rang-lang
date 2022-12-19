import sys

from rang_lang.parser import Parser
from rang_lang.scanner import Scanner
from rang_lang.transpiler import Transpiler


def main():

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
        parser.print_tree()

    elif py:
        parser.parse()
        transpiler = Transpiler(parser.tree)
        transpiler.compile_to_python()

    sys.exit()


def run_help():
    print("Command Syntax:")
    print("\t\t./rang_compiler [flags] filename")
    print("\nRequired arguments:")
    print("\t\tfilename is the pathname (absolute or relative) to the input file.")
    print("\nOptional flags:")
    print("\t\t-h\t\tprints this message")
    print("\nAt most one of the following three flags:")
    print("\t\t-s\t\tis the standard compiler")


if __name__ == "__main__":
    main()
