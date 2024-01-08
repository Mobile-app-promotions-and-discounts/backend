from django.core.management.base import BaseCommand, CommandError

from factories.products import (FavoritesFactory, ProductImageFactory,
                                ProductsInStoreFactory, ReviewFactory)

OBJECTS_COUNT = 20


class Command(BaseCommand):
    help = 'Создание тестовых данных для БД'

    def handle(self, *args, **options):
        try:
            self.stdout.write(self.style.SUCCESS('Начинаем генерацию тестовых данных...Ожидайте'))
            ProductsInStoreFactory.create_batch(OBJECTS_COUNT)
            self.stdout.write(self.style.SUCCESS('Были успешно сгенерированы продукты и магазины'))
            ProductImageFactory.create_batch(OBJECTS_COUNT)
            self.stdout.write(self.style.SUCCESS('Были успешно сгенерированы доп. картинки к товарам'))
            ReviewFactory.create_batch(OBJECTS_COUNT)
            self.stdout.write(self.style.SUCCESS('Были успешно сгенерированы отзывы на товары'))
            FavoritesFactory.create_batch(OBJECTS_COUNT)
            self.stdout.write(self.style.SUCCESS('Были успешно сгенерированы избранные товары'))
            self.stdout.write(self.style.SUCCESS('Создание тестовых данных успешно завершено!'))
        except CommandError as err:
            self.stdout.write(self.style.ERROR(f"Ошибка наполнения базы данных:\n{err}"))
