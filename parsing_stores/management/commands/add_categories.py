from django.core.management.base import BaseCommand
from products.models import Category


class Command(BaseCommand):
    help = 'Создание категорий товаров из вариантов выбора категорий'

    def handle(self, *args, **options):
        category_names = [category[0] for category in Category.CategoryType.choices]
        for category_name in category_names:
            Category.objects.get_or_create(name=category_name)
