"""Compatibility shim: re-export Utils class from utils.Utils module.
Some modules do `from Utils import Utils` (capitalized); provide that path.
"""
from utils.Utils import Utils

__all__ = ['Utils']
