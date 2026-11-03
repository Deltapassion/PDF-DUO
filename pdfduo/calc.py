"""Évaluateur d'expressions mathématiques sûr (sans eval) pour le tableur et la calculatrice.

Accepte : nombres (virgule ou point décimal), + - * / x × ÷ ^ et **, parenthèses,
√(…) ou racine(…), pourcentage « 50% », constantes pi / π / e, fonctions usuelles,
références de cellules (A1, B12) et plages (A1:B3) pour SOMME, MOYENNE, MIN, MAX, PRODUIT, NB.
"""
import ast
import warnings
import math
import re

DEG = {"on": False}           # mode degrés de la calculatrice (sin, cos, tan…)


class CalcError(Exception):
    pass


def _trig(f):
    return lambda x: f(math.radians(x)) if DEG["on"] else f(x)


def _atrig(f):
    return lambda x: math.degrees(f(x)) if DEG["on"] else f(x)


def _flat(args):
    out = []
    for a in args:
        if isinstance(a, (list, tuple)):
            out.extend(_flat(a))
        elif a is not None:
            out.append(a)
    return out


def _fact(x):
    if x < 0 or x != int(x) or x > 170:
        raise CalcError("factorielle")
    return float(math.factorial(int(x)))


def _root(x, n=2):
    if n == 2:
        if x < 0:
            raise CalcError("racine d'un nombre négatif")
        return math.sqrt(x)
    if x < 0 and int(n) == n and int(n) % 2 == 1:
        return -((-x) ** (1 / n))
    return x ** (1 / n)


def _log(x, b=10):
    return math.log(x, b)


def _round(x, n=0):
    return round(x, int(n))


FUNCS = {
    "sqrt": _root, "racine": _root, "rac": _root, "root": _root,
    "sin": _trig(math.sin), "cos": _trig(math.cos), "tan": _trig(math.tan),
    "asin": _atrig(math.asin), "acos": _atrig(math.acos), "atan": _atrig(math.atan),
    "arcsin": _atrig(math.asin), "arccos": _atrig(math.acos), "arctan": _atrig(math.atan),
    "sinh": math.sinh, "cosh": math.cosh, "tanh": math.tanh,
    "ln": math.log, "log": _log, "log10": math.log10, "log2": math.log2, "exp": math.exp,
    "abs": abs, "fact": _fact, "arrondi": _round, "round": _round,
    "ent": math.floor, "floor": math.floor, "ceil": math.ceil, "int": math.floor,
    "somme": lambda *a: float(sum(_flat(a))), "sum": lambda *a: float(sum(_flat(a))),
    "moyenne": lambda *a: (sum(_flat(a)) / len(_flat(a))) if _flat(a) else 0.0,
    "average": lambda *a: (sum(_flat(a)) / len(_flat(a))) if _flat(a) else 0.0,
    "min": lambda *a: min(_flat(a)), "max": lambda *a: max(_flat(a)),
    "produit": lambda *a: float(math.prod(_flat(a))), "product": lambda *a: float(math.prod(_flat(a))),
    "nb": lambda *a: float(len(_flat(a))), "count": lambda *a: float(len(_flat(a))),
}
CONSTS = {"pi": math.pi, "e": math.e}

_REF = re.compile(r"\b([A-Za-z]{1,2})([0-9]{1,4})\b")
_RANGE = re.compile(r"\b([A-Za-z]{1,2}[0-9]{1,4})\s*:\s*([A-Za-z]{1,2}[0-9]{1,4})\b")
MAX_LEN = 500
MAX_POW = 1e6


def col_name(c):
    s = ""
    c += 1
    while c:
        c, r = divmod(c - 1, 26)
        s = chr(65 + r) + s
    return s


def col_index(name):
    n = 0
    for ch in name.upper():
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def parse_ref(ref):
    m = re.fullmatch(r"([A-Za-z]{1,2})([0-9]{1,4})", ref.strip())
    if not m:
        return None
    return int(m.group(2)) - 1, col_index(m.group(1))


def normalize(expr, x_mult=True):
    """Texte saisi → syntaxe Python restreinte."""
    s = str(expr).strip()
    if s.startswith("="):
        s = s[1:].strip()
    if len(s) > MAX_LEN:
        raise CalcError("expression trop longue")
    s = (s.replace("×", "*").replace("÷", "/").replace("−", "-").replace("π", "pi")
         .replace("√", "sqrt").replace("²", "**2").replace("³", "**3").replace("^", "**"))
    # virgule décimale (3,5) ; le séparateur d'arguments est « ; »
    s = re.sub(r"(?<=\d),(?=\d)", ".", s)
    s = s.replace(";", ",")
    # « x » comme multiplication entre deux opérandes (2 x 3, 2x3, (1)x(2)) mais pas la variable x seule
    if x_mult:
        s = re.sub(r"(?<=[\d)])\s*[xX]\s*(?=[\d(A-Za-z])", "*", s)
    # pourcentage
    s = re.sub(r"(\d+(?:\.\d+)?)\s*%", r"(\1/100)", s)
    # sqrt9 → sqrt(9)
    s = re.sub(r"sqrt\s*(\d+(?:\.\d+)?)", r"sqrt(\1)", s)
    # multiplication implicite : 2(3), )(, 2pi, 2sqrt(…)
    s = re.sub(r"(\d)\s*\(", r"\1*(", s)
    s = re.sub(r"\)\s*\(", ")*(", s)
    s = re.sub(r"(\d)\s*(pi|sqrt|sin|cos|tan|ln|log|exp)\b", r"\1*\2", s)
    s = re.sub(r"\)\s*(\d)", r")*\1", s)
    return s.strip()


class _Eval:
    def __init__(self, names, ranges):
        self.names = names
        self.ranges = ranges

    def v(self, n):
        if isinstance(n, ast.Expression):
            return self.v(n.body)
        if isinstance(n, ast.Constant):
            if isinstance(n.value, (int, float)) and not isinstance(n.value, bool):
                return float(n.value)
            raise CalcError("valeur non numérique")
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, (ast.UAdd, ast.USub)):
            x = self.v(n.operand)
            return -x if isinstance(n.op, ast.USub) else x
        if isinstance(n, ast.BinOp):
            a, b = self.v(n.left), self.v(n.right)
            op = n.op
            if isinstance(op, ast.Add):
                return a + b
            if isinstance(op, ast.Sub):
                return a - b
            if isinstance(op, ast.Mult):
                return a * b
            if isinstance(op, ast.Div):
                if b == 0:
                    raise CalcError("division par zéro")
                return a / b
            if isinstance(op, ast.Mod):
                return a % b
            if isinstance(op, ast.Pow):
                if abs(b) > MAX_POW or (abs(a) > 1 and abs(b) * math.log10(abs(a)) > 300):
                    raise CalcError("nombre trop grand")
                try:
                    r = a ** b
                except (OverflowError, ZeroDivisionError):
                    raise CalcError("nombre trop grand")
                if isinstance(r, complex):
                    raise CalcError("résultat complexe")
                return r
            raise CalcError("opérateur non permis")
        if isinstance(n, ast.Name):
            k = n.id
            if k in self.names:
                return self.names[k]
            kl = k.lower()
            if kl in CONSTS:
                return CONSTS[kl]
            if k in self.ranges:
                raise CalcError("plage hors d'une fonction (ex. SOMME(A1:A3))")
            raise CalcError(f"nom inconnu : {k}")
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and not n.keywords:
            f = FUNCS.get(n.func.id.lower())
            if f is None:
                raise CalcError(f"fonction inconnue : {n.func.id}")
            args = [self.v(a) if not (isinstance(a, ast.Name) and a.id in self.ranges)
                    else self.ranges[a.id] for a in n.args]
            if len(args) > 1000:
                raise CalcError("trop d'arguments")
            try:
                r = f(*args)
            except CalcError:
                raise
            except (ValueError, TypeError, ZeroDivisionError, OverflowError):
                raise CalcError("calcul impossible")
            return float(r)
        raise CalcError("expression non permise")


def evaluate(expr, names=None, cell_value=None):
    """Calcule une expression. cell_value(r, c) → float ou None fournit les cellules du tableau."""
    s = normalize(expr)
    ranges = {}
    if cell_value is not None:
        def rng(m):
            a, b = parse_ref(m.group(1)), parse_ref(m.group(2))
            r0, r1 = sorted((a[0], b[0]))
            c0, c1 = sorted((a[1], b[1]))
            if (r1 - r0 + 1) * (c1 - c0 + 1) > 10000:
                raise CalcError("plage trop grande")
            vals = [cell_value(r, c) for r in range(r0, r1 + 1) for c in range(c0, c1 + 1)]
            key = f"_R{len(ranges)}"
            ranges[key] = [v for v in vals if v is not None]
            return key
        s = _RANGE.sub(rng, s)
        refs = {}

        def ref(m):
            name = m.group(0)
            low = name.lower()
            if low in FUNCS or low in CONSTS or name.startswith("_R"):
                return name
            rc = parse_ref(name)
            v = cell_value(*rc)
            key = "_C" + name.upper()
            refs[key] = 0.0 if v is None else v
            return key
        s = _REF.sub(ref, s)
        names = dict(names or {}, **refs)
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            tree = ast.parse(s, mode="eval")
    except (SyntaxError, ValueError, RecursionError, MemoryError):
        raise CalcError("syntaxe incorrecte")
    try:
        r = _Eval(names or {}, ranges).v(tree)
    except RecursionError:
        raise CalcError("expression trop complexe")
    except OverflowError:
        raise CalcError("nombre trop grand")
    if isinstance(r, float) and (math.isnan(r) or math.isinf(r)):
        raise CalcError("résultat indéfini")
    return r


def compile_fx(expr):
    """Prépare f(x) pour le traceur de courbes. Renvoie une fonction x → float ou None."""
    s = normalize(expr, x_mult=False)
    s = re.sub(r"^\s*[yf]\s*(\(\s*x\s*\))?\s*=", "", s)
    s = re.sub(r"(\d)\s*x\b", r"\1*x", s)
    s = re.sub(r"\bx\s*\(", "x*(", s)
    s = re.sub(r"\)\s*x\b", ")*x", s).strip()
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            tree = ast.parse(s, mode="eval")
    except (SyntaxError, ValueError, RecursionError, MemoryError):
        raise CalcError("syntaxe incorrecte")
    ev = _Eval({"x": 0.0}, {})

    def f(x):
        ev.names = {"x": float(x), "X": float(x)}
        try:
            r = ev.v(tree)
        except (CalcError, ValueError, TypeError, ZeroDivisionError, OverflowError, RecursionError):
            return None
        if math.isnan(r) or math.isinf(r):
            return None
        return r
    # vérifie les noms une fois (x = 1)
    ev.names = {"x": 1.0, "X": 1.0}
    try:
        ev.v(tree)
    except CalcError as e:
        if "inconnu" in str(e) or "non permis" in str(e) or "non numérique" in str(e):
            raise
    except (ValueError, ZeroDivisionError, OverflowError, RecursionError, TypeError):
        pass
    return f


def fmt(v, digits=10):
    if v is None:
        return ""
    if abs(v - round(v)) < 1e-9 and abs(v) < 1e15:
        return str(int(round(v)))
    s = f"{v:.{digits}g}"
    return s
