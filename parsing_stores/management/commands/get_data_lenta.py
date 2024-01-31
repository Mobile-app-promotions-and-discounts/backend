import asyncio
from django.core.management.base import BaseCommand

from parsing_stores.lenta.main import main_


class Command(BaseCommand):
    help = 'Парсинг и загрузка данных из магазинов Лента'

    def handle(self, *args, **options):
        asyncio.run(main_())
