from __future__ import annotations
from typing import Any

def bval(value: Any) -> int:
    if isinstance(value, int):
        return value
    if isinstance(value, (bytes, bytearray)):
        return value[0]
    return ord(value)


def ensure_text(value: Any, encoding: str = 'utf-8', errors: str = 'replace') -> str:
    if value is None:
        return ''
    if isinstance(value, str):
        return value
    if isinstance(value, (bytes, bytearray)):
        try:
            return bytes(value).decode(encoding)
        except Exception:
            try:
                return bytes(value).decode('utf-8', errors)
            except Exception:
                return bytes(value).decode('latin1', errors)
    return str(value)


def ensure_bytes(value: Any, encoding: str = 'utf-8', errors: str = 'replace') -> bytes:
    if value is None:
        return b''
    if isinstance(value, bytes):
        return value
    if isinstance(value, bytearray):
        return bytes(value)
    if isinstance(value, str):
        return value.encode(encoding, errors)
    return str(value).encode(encoding, errors)


def exec_config(path: str, target: Any) -> None:
    namespace = {'self': target}
    with open(path, 'rb') as fh:
        code = compile(fh.read(), path, 'exec')
    exec(code, namespace, namespace)


def exec_script(source: str, extra_globals: dict | None = None) -> None:
    namespace = {'__name__': '__main__'}
    if extra_globals:
        namespace.update(extra_globals)
    exec(compile(source, '<cli-snippet>', 'exec'), namespace, namespace)
