import ast

from rang_lang.astnodes.program import Program


class Transpiler:
    def __init__(self, tree: Program):
        self.tree = tree

    def build_py_ast(self):
        body = []
        for stmt in self.tree.get_statements():
            body.append(stmt.to_py_ast())
        tree = ast.Module(body=body, type_ignores=[])
        ast.fix_missing_locations(tree)
        return tree
