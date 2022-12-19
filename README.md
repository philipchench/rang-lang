# rang-lang
Rang is my DIY programming language. Supports basic arithmetics, int/float/boolean, conditionals, while loops, 
function definitions, function calls, built-in functions for basic math and stdout.

## how to run:
Download the repo. run the shell script ./rangc after modifying permissions.
Syntax: ./rangc <flag> <filepath>
flag:
-py: converts Rang code into Python AST, compiles and executes it.
-p: prints Python AST to stdout, doesn't compile nor execute.
filepath: the file path

## about the transpiler
This program is made of several parts: a scanner/parser frontend, Rang AST node representations, 
and the transpiler that converts the Rang AST into a Python AST using the ast module, 
which then gets compiled and executed (in Python of course). The scanner simply builds a list of tokens. 
After scanning, the recursive-descent parser builds the syntax tree, which is represented by AST nodes 
starting with Program() as the root. The transpiler can then build a Python module AST from the Program()'s 
list of statements, and finally, the code is executed. The parser picks up basic syntax errors, while 
Python picks up whatever is left, as Rang is technically an interpreted language.

## about Rang
Rang is inspired by C syntax and can look quite similar to Javascript. A few things to note: module has the 
same precedence level as multiplication; // is for comments so there is no Python floor division; semicolons 
are optional for blocks with curly brackets; whatever else weird behavior is Python's fault. \s
Built-in functions:
out(*args): exactly the same as print() in Python3.
floor(x): pretty much int(x), but emphasis on the "floor" for the lack of a primitive floor division operator.
power(x, y): essentially x ** y.

EBNF grammar is located in notes/task02-cond-iter-func.txt