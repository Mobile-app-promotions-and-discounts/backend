from datetime import datetime

from django.core.management.base import BaseCommand
from parsing_stores.magnit.magnit_parsing import main


class Command(BaseCommand):
    help = 'Парсинг и загрузка данных из магазинов Магнит'

    def handle(self, *args, **options):
        print('Начало работы парсинга Магнит.')
        start = datetime.today()
        main()
        print(f'Парсинг окончен за {datetime.today() - start}.')
