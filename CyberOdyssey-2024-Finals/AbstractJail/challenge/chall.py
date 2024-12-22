import ast
import sys

BANNED_NODES = {
    ast.Expression,
    ast.Interactive,
    ast.FunctionType,
    ast.FunctionDef,
    ast.AsyncFunctionDef,
    ast.ClassDef,
    ast.Return,
    ast.Delete,
    ast.Assign,
    ast.AugAssign,
    ast.AnnAssign,
    ast.For,
    ast.AsyncFor,
    ast.While,
    ast.If,
    ast.With,
    ast.AsyncWith,
    ast.Raise,
    ast.Try,
    ast.Assert,
    ast.Import,
    ast.ImportFrom,
    ast.Global,
    ast.Nonlocal,
    ast.Pass,
    ast.Break,
    ast.Continue,
    ast.BoolOp,
    ast.UnaryOp,
    ast.Lambda,
    ast.IfExp,
    ast.Dict,
    ast.Set,
    ast.ListComp,
    ast.SetComp,
    ast.DictComp,
    ast.GeneratorExp,
    ast.Await,
    ast.Yield,
    ast.YieldFrom,
    ast.Compare,
    ast.Constant,
    ast.Attribute,
    ast.Subscript,
    ast.Starred,
    ast.List,
    ast.Tuple,
    ast.Slice,
    ast.Mod,
    ast.Pow,
    ast.LShift,
    ast.RShift,
    ast.BitOr,
    ast.BitXor,
    ast.BitAnd,
    ast.FloorDiv,
    ast.Eq,
    ast.NotEq,
    ast.Lt,
    ast.LtE,
    ast.Gt,
    ast.GtE,
    ast.Is,
    ast.IsNot,
    ast.In,
    ast.NotIn,
    ast.And,
    ast.Or,
    ast.Not,
    ast.alias,
    ast.withitem,
    ast.arguments,
    ast.arg,
    ast.keyword,
    ast.comprehension,
    ast.ExceptHandler,
    ast.Match,
    ast.match_case,
    ast.JoinedStr,
    ast.FormattedValue
}

BANNED_WORDS = [
    'ast',
    'audit',
    'cat',
    'compile',
    'exec',
    'flag',
    'fork',
    'frame',
    'hook',
    'import',
    'open',
    'os',
    'print',
    'sh',
    'spawn',
    'subprocess',
    'sys'
]

def hook(event, args):
    global first_audit
    
    if first_audit:
        first_audit = False
        return
    
    audit_str = (event + " " + " ".join(map(str, args))).lower()
    
    if any(word in audit_str for word in BANNED_WORDS):
        audit_msg = f"Security violation detected: {event} {' '.join(map(str, args))}"
        print(audit_msg)
        exit()

def validate_ast(code_str):
    try:
        tree = ast.parse(code_str)
        for node in ast.walk(tree):
            if type(node) in BANNED_NODES:
                print(f"Invalid node: {type(node).__name__}")
                return False
        return True
    except SyntaxError:
        print("Invalid syntax!")
        return False

def read_program():
    print("""
    ╔═══════════════════════════════════╗
    ║           ABSTRACT JAIL           ║
    ║         No Escape Allowed         ║
    ║                                   ║
    ║      ▒▒▒▒▒    ▒▒▒▒▒    ▒▒▒▒▒      ║
    ║      ▒   ▒    ▒   ▒    ▒   ▒      ║
    ║      ▒   ▒    ▒   ▒    ▒   ▒      ║
    ║      ▒▒▒▒▒    ▒▒▒▒▒    ▒▒▒▒▒      ║
    ║                                   ║
    ╚═══════════════════════════════════╝

Welcome prisoner! Submit your code for inspection:
""")
    lines = []
    while True:
        line = input("")
        if line == "EOF":
            break
        lines.append(line)
    return "\n".join(lines)

first_audit = True

code = read_program()

if not validate_ast(code):
    exit()

code = compile(code, "AbstractJail", "exec")

sys.addaudithook(hook)

exec(code)
