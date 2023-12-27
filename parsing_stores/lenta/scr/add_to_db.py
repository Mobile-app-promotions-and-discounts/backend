import logging
from django.core.files.base import ContentFile

from parsing_stores.lenta.scr.core import get_response
import parsing_stores.lenta.scr.msg as msg
from products.models import (Category,
                             ChainStore,
                             Discount,
                             Product,
                             ProductsInStore,
                             Store,
                             StoreLocation)


logger = logging.getLogger()


def add_category(category_data):
    """Подготовка картинки для db"""
    if Category.objects.filter(name=category_data).exists():
        return Category.objects.get(name=category_data)
    else:
        logger.debug(msg.CATEGORY_NOT_FOUND.format(category_data))


def add_image(url):
    """Подготовка картинки для db"""
    response = get_response(options={'url': url})
    return response.content


def add_store(store_data):
    """Подготовка магазина для db"""
    return Store(
        name=store_data.get('name'),
        location=StoreLocation(**store_data.get('location')),
        chain_store=ChainStore(**store_data.get('chain_store'))
    )


def add_products(product_data):
    """Подготовка продукта для db"""
    category_data = product_data.pop('category')

    if product_data.get('main_image'):
        main_image = product_data.pop('main_image')[0]
        image = add_image(main_image)
    else:
        image = None
    category = add_category(category_data)

    if not Product.objects.filter(category=category, **product_data).exists():
        return Product(
            category=category,
            main_image=ContentFile(image, name='img.jpeg'),
            **product_data,
        )
    return Product.objects.get(
        category=category,
        **product_data,
    )


def add_to_db(all_products_in_store, store_data):
    data = []

    for products_in_store in all_products_in_store:
        product_data = products_in_store.pop('product')
        discount_data = products_in_store.pop('discount')

        product = add_products(product_data)
        store = add_store(store_data)

        data.append(
            ProductsInStore(
                product=product,
                store=store,
                discount=Discount(**discount_data),
                **products_in_store,
            )
        )
    ProductsInStore.objects.bulk_create(data)
