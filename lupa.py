"""Minimal stub for lupa.LuaRuntime used for local testing.

This does not implement real Lua; it only provides the methods accessed by
modules/Lua.py during server initialization so imports succeed.
"""
class LuaTable(dict):
    def __len__(self):
        return dict.__len__(self)


class LuaRuntime:
    def __init__(self, *args, **kwargs):
        self._globals = LuaTable()
        # Provide nested tables used by Lua.SetupRuntimeGlobals
        self._globals.setdefault('table', {})
        self._globals.setdefault('os', {})
        self._globals.setdefault('ui', {})
        self._globals.setdefault('tfm', {})

    def globals(self):
        return self._globals

    def eval(self, expr):
        # Return a new LuaTable for constructs like 'setmetatable({}, ... )'
        return LuaTable()
