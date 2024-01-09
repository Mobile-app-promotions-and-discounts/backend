from datetime import datetime

from django.core.management.base import BaseCommand

from parsing_stores.magnit.get_stores import main
from products.models import Store


class Command(BaseCommand):
    help = 'Загрузка магазинов в базу данных'

    def handle(self, *args, **options):
        print('Добавление магазинов сети "Магнит"')
        start = datetime.today()
        amount_stores_magnit_start = Store.objects.filter(chain_store__name='Магнит').count()
        main()
        amount_stores_magnit = Store.objects.filter(chain_store__name='Магнит').count()
        print(f'Добавлено {amount_stores_magnit - amount_stores_magnit_start} магазинов за {datetime.today() - start}.')
