class CursorShim:
    """Um shim mínimo de cursor para evitar erros durante desenvolvimento local.
    Ele aceita chamadas execute/fetchone/fetchall e retorna valores vazios.
    """
    def __init__(self, name="shim"):
        self.name = name
        self.lastrowid = 0

    def execute(self, query, params=None):
        # Apenas registra (poderíamos imprimir em debug se necessário)
        return None

    def fetchone(self):
        class RowShim:
            def __getitem__(self, key):
                # Se index numérico for pedido, retorne 0
                if isinstance(key, int):
                    return 0
                # Para chaves de coluna, retornar string vazia
                return ""

            def get(self, key, default=None):
                return default if default is not None else ""

            def keys(self):
                return []

            def items(self):
                return []

            def __iter__(self):
                return iter([])

        return RowShim()

    def fetchall(self):
        return []

    def __iter__(self):
        return iter([])

    def close(self):
        pass
