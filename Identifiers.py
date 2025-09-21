"""Compatibility shim: re-export Identifiers from modules.Identifiers.

Some modules import `from Identifiers import Identifiers` while others import
`from modules.Identifiers import Identifiers`. Provide both paths by reusing
the stub in modules/Identifiers.py.
"""
from modules.Identifiers import Identifiers

__all__ = ['Identifiers']
