"""Compatibility shim re-exporting modules.ByteArray.ByteArray
so both `from modules.ByteArray import ByteArray` and
`from ByteArray import ByteArray` work during local testing.
"""
from modules.ByteArray import ByteArray

__all__ = ['ByteArray']
