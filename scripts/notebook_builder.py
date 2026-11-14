import ast
import builtins
import textwrap


class Cell:
    def __init__(self, code, hide=True, cell_id=None):
        self.code = textwrap.dedent(code).strip()
        self.hide = hide
        self.cell_id = cell_id


def _top_defs(body):
    names = set()

    def target(node):
        if isinstance(node, ast.Name):
            names.add(node.id)
        elif isinstance(node, (ast.Tuple, ast.List)):
            for elt in node.elts:
                target(elt)

    for node in body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                target(t)
        elif isinstance(node, (ast.AnnAssign, ast.AugAssign)):
            target(node.target)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                names.add((alias.asname or alias.name).split(".")[0])
        elif isinstance(node, (ast.For, ast.AsyncFor)):
            target(node.target)
            names |= _top_defs(node.body) | _top_defs(node.orelse)
        elif isinstance(node, ast.If):
            names |= _top_defs(node.body) | _top_defs(node.orelse)
        elif isinstance(node, (ast.With, ast.AsyncWith)):
            for item in node.items:
                if item.optional_vars is not None:
                    target(item.optional_vars)
            names |= _top_defs(node.body)
        elif isinstance(node, ast.Try):
            names |= _top_defs(node.body) | _top_defs(node.orelse) | _top_defs(node.finalbody)
            for handler in node.handlers:
                if handler.name:
                    names.add(handler.name)
                names |= _top_defs(handler.body)
    return names


def analyze(cells):
    """Return (defs, refs) per cell, using marimo's rule that _names are cell-private."""
    trees = [ast.parse(c.code) for c in cells]
    defs = [{n for n in _top_defs(t.body) if not n.startswith("_")} for t in trees]
    everything = set().union(*defs)
    owner = {}
    for i, names in enumerate(defs):
        for name in names:
            if name in owner:
                raise ValueError(f"{name} is defined in two cells")
            owner[name] = i
    refs = []
    for i, tree in enumerate(trees):
        loads = {
            n.id for n in ast.walk(tree) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)
        }
        refs.append(sorted((loads & everything) - defs[i] - set(dir(builtins))))
    return defs, refs, owner


def render(cells):
    defs, refs, _ = analyze(cells)
    out = []
    for cell, names, args in zip(cells, defs, refs):
        returns = "return (" + ", ".join(sorted(names)) + ",)" if names else "return"
        decorator = "@app.cell(hide_code=True)" if cell.hide else "@app.cell"
        body = textwrap.indent(cell.code + "\n" + returns, "    ")
        identity = f"# workshop-cell: {cell.cell_id}\n" if cell.cell_id else ""
        out.append(f"\n\n{identity}{decorator}\ndef _({', '.join(args)}):\n{body}\n")
    return "".join(out)
