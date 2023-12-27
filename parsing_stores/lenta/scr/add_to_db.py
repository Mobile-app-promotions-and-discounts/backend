import logging
from django.core.files.base import ContentFile

from scr.core import get_response
import scr.msg as msg
from products.models import (Category,
                             Product,
                             ProductsInStore,
                             Store)


logger = logging.getLogger()


def add_category(category):
    """Подготовка картинки для db"""
    if Category.objects.filter(name=category).exists():
        return Category.objects.get(name=category)
    else:
        logger.debug(msg.CATEGORY_NOT_FOUND.format(category))


def add_image(url):
    """Подготовка картинки для db"""
    response = get_response(options={'url': url})
    return response.content


def add_products(data, category):
    """Подготовка продукта для db"""
    if not Product.objects.filter(category=category, **data).exists():
        return Product.objects.create(
            category=category,
            main_image=ContentFile(
                add_image(data.get('main_image')[0] if data.get('main_image') else None),
                name='img.jpeg'
            ),
            **data,
        )
    return Product.objects.get(
        category=category,
        **data,
    )


def add_to_db():
    data = []

    ProductsInStore.objects.get_or_create(
            product=prod,
            store=store,
            discount=disc,
            **price_in_store,
        )
    
    ProductsInStore.objects.bulk_create(ingredients_obj)
