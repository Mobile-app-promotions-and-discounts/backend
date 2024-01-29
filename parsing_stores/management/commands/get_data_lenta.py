from django.core.management.base import BaseCommand
from parsing_stores.lenta.main import main


class Command(BaseCommand):
    help = 'Парсинг и загрузка данных из магазинов Лента'

    def handle(self, *args, **options):
        main()
