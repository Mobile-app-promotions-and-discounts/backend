from datetime import datetime

from django.core.management.base import BaseCommand

from parsing_stores.magnit.add_in_db_ii import run_add_data_in_db


class Command(BaseCommand):
    help = 'Парсинг и загрузка данных из магазинов Магнит'

    def handle(self, *args, **options):
        print('Начало работы парсинга Магнит.')
        start = datetime.today()
        run_add_data_in_db()
        print(f'Парсинг окончен за {datetime.today() - start}.')
