
import importlib
import types

class MissingModule(types.SimpleNamespace):
    def __init__(self, name, error=None):
        super().__init__()
        self.__name__ = name
        self._error = error
    def __getattr__(self, item):
        def _missing(*args, **kwargs):
            raise RuntimeError(f"Optional module {self.__name__} is not available: {self._error}")
        return _missing

def optional_import(name):
    try:
        return importlib.import_module(name)
    except Exception as e:
        print(f"Optional import failed: {name}: {e}")
        return MissingModule(name, e)
