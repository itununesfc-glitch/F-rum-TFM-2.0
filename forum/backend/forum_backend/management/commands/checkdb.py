from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError

class Command(BaseCommand):
    help = 'Verifica a conexão com o banco de dados e exibe uma mensagem de sucesso.'

    def handle(self, *args, **options):
        db_conn = connections['default']
        try:
            db_conn.cursor()
            self.stdout.write(self.style.SUCCESS('Conexão com o banco de dados funcionando perfeitamente!'))
        except OperationalError:
            self.stdout.write(self.style.ERROR('Não foi possível conectar ao banco de dados.'))
