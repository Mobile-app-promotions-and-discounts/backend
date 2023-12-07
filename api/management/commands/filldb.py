from django.core.management.base import BaseCommand, CommandError

from factories.products import (FavoritesFactory, ProductFactory,
                                ProductsInStoreFactory, ReviewFactory)


class Command(BaseCommand):
    help = 'Создание тестовых данных для БД'

    def handle(self, *args, **options):
        try:
            self.stdout.write(self.style.SUCCESS('Начинаем генерацию тестовых данных...Ожидайте'))
            ProductsInStoreFactory.create_batch(20)
            ProductFactory.create_batch(20)
            ReviewFactory.create_batch(10)
            FavoritesFactory.create_batch(10)
            self.stdout.write(self.style.SUCCESS('Создание тестовых данных успешно завершено!'))
        except CommandError as err:
            self.stdout.write(self.style.ERROR(f"Ошибка наполнения базы данных:\n{err}"))
