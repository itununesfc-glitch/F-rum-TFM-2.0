__all__ = []
__all__ = []

import pkgutil
import inspect
import importlib

__all__ = []

for loader, name, is_pkg in pkgutil.walk_packages(__path__):
    # Try to import submodule; if it fails (missing deps) skip it so the package
    # can still be imported for testing/partial execution.
    try:
        module = importlib.import_module(f"{__name__}.{name}")
    except Exception:
        # Skip modules that can't be imported (e.g., require native libs)
        continue

    for member_name, value in inspect.getmembers(module):
        if member_name.startswith('__'):
            continue
        globals()[member_name] = value
        __all__.append(member_name)
