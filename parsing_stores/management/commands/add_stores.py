import csv

from datetime import datetime

from django.core.management.base import BaseCommand

from products.models import ChainStore, Store, StoreLocation
from parsing_stores.magnit.get_stores import main


class Command(BaseCommand):
    help = 'Загрузка магазинов в базу данных'

    def add_arguments(self, parser):
        parser.add_argument('path_file', type=str)

    def handle(self, *args, **options):
        print('Добавление магазинов сети "Магнит"')
        start = datetime.today()
        amount_stores_magnit_start = Store.objects.filter(chain_store__name='Магнит').count()
        main()
        amount_stores_magnit = Store.objects.filter(chain_store__name='Магнит').count()
        print(f'Добавлено {amount_stores_magnit - amount_stores_magnit_start} магазинов за {datetime.today() - start}.')

    # def handle(self, *args, **kwargs):
    #     if kwargs['path_file'].endswith('.csv'):
    #         with open(kwargs['path_file'], 'r') as file:
    #             stores = csv.DictReader(file)
    #             location = {}
    #             for store in stores:
    #                 location['region'] = store.pop('region')
    #                 location['city'] = store.pop('city')
    #                 location['address'] = store.pop('address')
    #                 location['latitude'] = store.pop('latitude')
    #                 location['longitude'] = store.pop('longitude')
    #                 chain_store_name = store.pop('chain_store')
    #                 chain_store = ChainStore.objects.get_or_create(name=chain_store_name)
    #                 store_location = StoreLocation.objects.get_or_create(**location)
    #                 Store.objects.get_or_create(
    #                     chain_store=chain_store[0],
    #                     location=store_location[0],
    #                     **store,
    #                 )
