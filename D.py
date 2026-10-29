"""
D - Difficulty
==============

Librería Python de un solo archivo, EXTREMADAMENTE difícil de usar.
No hay documentación. No hay ayuda. Solo existe D.

    >>> import D
    >>> D.???

Suerte.
"""

import base64 as _b64
import zlib as _z
import hashlib as _hl
import sys as _sys

__all__ = ['D', '__version__']


# ---------------------------------------------------------------------------
# Codificación (para que nada sea legible a simple vista)
# ---------------------------------------------------------------------------

def _e(s: str) -> str:
    return _b64.b85encode(_z.compress(s.encode('utf-8'))).decode('ascii')


def _d(s: str) -> str:
    return _z.decompress(_b64.b85decode(s.encode('ascii'))).decode('utf-8')


__version__ = "0.1." + str(len(_e("difficulty")) % 100)


if _sys.version_info < (3, 7):
    raise RuntimeError(_d(_e("Python 3.7+ required")))


# ---------------------------------------------------------------------------
# Estado global (sí, mutable, sí, oculto)
# ---------------------------------------------------------------------------

class _S:
    level = 1
    calls = 0
    unlocked = False
    attempts = 0
    _pw = _d(_e("open sesame"))    # <- pista escondida

    @classmethod
    def bump(cls):
        cls.calls += 1

    @classmethod
    def reset(cls):
        cls.level = 1
        cls.calls = 0
        cls.unlocked = False
        cls.attempts = 0


# ---------------------------------------------------------------------------
# Symbol: cada atributo desconocido de D devuelve uno de estos
# ---------------------------------------------------------------------------

class _Symbol:
    __slots__ = ('_path',)

    def __init__(self, path):
        self._path = path

    def __call__(self, *a, **k):
        return _dispatch(self._path, a, k)

    def __getattr__(self, name):
        if name.startswith('__') and name.endswith('__'):
            raise AttributeError(name)
        return _Symbol(f"{self._path}.{name}")

    def __getitem__(self, key):
        return _dispatch(self._path + '@get', (key,), {})

    def __repr__(self):
        return f"<D/{self._path}>"

    def __bool__(self):
        return True

    def __or__(self, other):
        return _Symbol(f"({self._path} | {other!r})")

    def __and__(self, other):
        return _Symbol(f"({self._path} & {other!r})")

    def __hash__(self):
        return hash(self._path)


# ---------------------------------------------------------------------------
# Resultado "encriptado" (nivel 5)
# ---------------------------------------------------------------------------

class _Encoded:
    __slots__ = ('_v',)

    def __init__(self, v):
        self._v = v

    def get(self):
        return self._v

    def __repr__(self):
        h = _hl.md5(str(self._v).encode()).hexdigest()[:8]
        return f"<_Encoded #{h}>"

    def __int__(self):
        return int(self._v)

    def __str__(self):
        return str(self._v)


# ---------------------------------------------------------------------------
# Operaciones aritméticas "normales" (según el nivel)
# ---------------------------------------------------------------------------

def _reverse_int(n):
    if n == 0:
        return 0
    sign = -1 if n < 0 else 1
    s = str(abs(n))[::-1]
    return sign * int(s)


def _op_add(args, kwargs, lvl):
    if lvl == 1:
        return sum(args) if args else 0
    if lvl == 2:
        if set(kwargs) == {'a', 'b'} and not args:
            return kwargs['a'] + kwargs['b']
        raise TypeError("add() en nivel 2 exige kwargs a=, b=")
    if lvl == 3:
        r = sum(args) if args else 0
        return _reverse_int(r) if isinstance(r, int) else r
    if lvl == 4:
        if not _S.unlocked:
            raise PermissionError("locked. usa D.unlock(pw)")
        return sum(args) if args else 0
    if lvl == 5:
        if not _S.unlocked:
            raise PermissionError("locked. usa D.unlock(pw)")
        return _Encoded(sum(args) if args else 0)
    return sum(args) if args else 0


def _op_sub(args, kwargs, lvl):
    if lvl == 1 and len(args) == 2:
        return args[0] - args[1]
    return args[0] - args[1] if len(args) == 2 else 0


def _op_mul(args, kwargs, lvl):
    r = 1
    for a in args:
        r *= a
    return r


def _op_pow(args, kwargs, lvl):
    return args[0] ** args[1] if len(args) == 2 else 0


# ---------------------------------------------------------------------------
# Dispatcher: el corazón de todo
# ---------------------------------------------------------------------------

def _dispatch(name, args, kwargs):
    _S.bump()
    lvl = _S.level

    if name == 'hello':
        return _d(_e("hello, world"))

    if name == 'add':
        return _op_add(args, kwargs, lvl)
    if name == 'sub':
        return _op_sub(args, kwargs, lvl)
    if name == 'mul':
        return _op_mul(args, kwargs, lvl)
    if name == 'pow':
        return _op_pow(args, kwargs, lvl)

    if name == 'state':
        return {
            'level': _S.level,
            'calls': _S.calls,
            'unlocked': _S.unlocked,
            'attempts': _S.attempts,
        }

    if name == 'level':
        if not args:
            return _S.level
        try:
            n = int(args[0])
        except Exception:
            return False
        if 1 <= n <= 5:
            _S.level = n
            return True
        return False

    if name == 'unlock':
        _S.attempts += 1
        if args and args[0] == _S._pw:
            _S.unlocked = True
            return True
        return False

    if name == 'secret':
        if _S.unlocked:
            return _d(_e("the cake is a lie"))
        return "locked"

    if name == 'reset':
        _S.reset()
        return True

    if name == 'puzzle':
        return _d(_e(
            "Niveles 4 y 5 estan bloqueados. "
            "Para desbloquear, llama D.unlock(pw). "
            "La contrasena esta escondida en el codigo fuente. "
            "Pista: son dos palabras, minusculas, separadas por espacio."
        ))

    if name == 'help':
        return "No."

    if name == 'reveal':
        return _d(_e("Revelado: nada. La dificultad es el punto."))

    return _Symbol(name)


# ---------------------------------------------------------------------------
# D
# ---------------------------------------------------------------------------

class _DMeta(type):
    def __getattr__(cls, name):
        if name.startswith('_'):
            raise AttributeError(name)
        return _Symbol(name)

    def __repr__(cls):
        return "<module D: Difficulty>"

    def __call__(cls, *a, **k):
        return _Symbol("()")


class D(metaclass=_DMeta):
    """El único. Suerte."""


# ---------------------------------------------------------------------------
# __getattr__ a nivel de módulo (PEP 562) - para confusión máxima
# ---------------------------------------------------------------------------

def __getattr__(name):
    if name.startswith('__'):
        raise AttributeError(name)
    return getattr(D, name)


def __dir__():
    return ['D', '__version__', 'hello', 'add', 'sub', 'mul', 'pow',
            'level', 'unlock', 'secret', 'state', 'reset', 'puzzle',
            'reveal', 'help']