"""Script de inicialização em modo de desenvolvimento.
Configura cursores shims e inicia o servidor para testar importações e handshake.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dev_db import CursorShim

# Criar shims e colocá-los no escopo do módulo MainServer antes da importação
# para que qualquer uso durante a importação não cause NoneType errors.
import types
import importlib

# Inserir um módulo temporal no sys.modules para que MainServer ao importar
# encontre os nomes Cursor, CursorCafe, CursorMaps definidos no próprio
# namespace do módulo após import — iremos setá-los logo após importar.

try:
    # Importar MainServer após termos shims prontos
    import MainServer
    MainServer.Cursor = CursorShim("main")
    MainServer.CursorCafe = CursorShim("cafe")
    MainServer.CursorMaps = CursorShim("maps")
except Exception as e:
    print("Falha ao iniciar o Server em modo dev:", e)

def start():
    # Instanciar o servidor de forma controlada (cuidado: roda loop.run_forever)
    try:
        srv = MainServer.Server()
    except Exception as e:
        import traceback
        print("Falha ao instanciar Server:", e)
        traceback.print_exc()

if __name__ == '__main__':
    start()
