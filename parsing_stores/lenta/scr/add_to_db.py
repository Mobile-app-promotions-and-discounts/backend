import logging

import backoff
from django.core.files.base import ContentFile
from django.db.utils import DatabaseError
from requests import Response

import parsing_stores.lenta.scr.config as cfg
from parsing_stores.lenta.scr.core import get_response
from products.models import (Category, ChainStore, Discount, Product,
                             ProductsInStore, Store, StoreLocation)

logger = logging.getLogger()

LOG_START_ADD_TO_DB = 'Начало добавления данных в DB...'
LOG_ADD_TO_DB = 'add_to_db - OK'


@backoff.on_exception(backoff.expo, exception=[DatabaseError,], logger=logger)
def add_category(category_data: dict) -> Category:
    """Подготовка картинки для db"""
    if not Category.objects.filter(name=category_data).exists():
        Category.objects.create(name=category_data)
    return Category.objects.get(name=category_data)


@backoff.on_exception(backoff.expo, exception=[DatabaseError,], logger=logger)
def add_image(url: str) -> bytes:
    """Подготовка картинки для db"""
    response: Response = get_response(
        options={'url': url, 'cookies': cfg.COOKIES, 'headers': cfg.HEADERS})
    return response.content


@backoff.on_exception(backoff.expo, exception=[DatabaseError,], logger=logger)
def add_store(store_data: dict) -> Store:
    """Подготовка магазина для db"""
    return Store.objects.get_or_create(
        name=store_data.get('name'),
        location=StoreLocation.objects.get_or_create(**store_data.get('location'))[0],
        chain_store=ChainStore.objects.get_or_create(**store_data.get('chain_store'))[0]
    )[0]


@backoff.on_exception(backoff.expo, exception=[DatabaseError,], logger=logger)
def add_products(product_data: dict) -> Product:
    """Подготовка продукта для db"""
    category_data: str = product_data.pop('category', None)

    if product_data.get('main_image'):
        main_image: str = product_data.pop('main_image', None)[0]
        image: bytes = add_image(main_image)
        _image: ContentFile = ContentFile(image, name='img_product.jpeg')
    else:
        _image = None
    category: Category = add_category(category_data)

    if not Product.objects.filter(category=category, **product_data).exists():
        return Product.objects.create(
            category=category,
            main_image=_image,
            **product_data
        )
    return Product.objects.get(
        category=category,
        **product_data
    )


@backoff.on_exception(backoff.expo,
                      exception=[DatabaseError,],
                      logger=logger)
def add_to_db(all_products_in_store: list, store_data: dict) -> None:
    """Заполнеиние БД ProductsInStore"""
    logger.debug(LOG_START_ADD_TO_DB)
    data = []
    store: Store = add_store(store_data)
    for products_in_store in all_products_in_store:
        product_data: dict = products_in_store.pop('product', None)
        discount_data: dict = products_in_store.pop('discount', None)
        product: Product = add_products(product_data)
        data.append(
            ProductsInStore(
                store=store,
                product=product,
                discount=Discount.objects.get_or_create(**discount_data)[0],
                **products_in_store,
            )
        )
    ProductsInStore.objects.bulk_create(data,
                                        update_conflicts=True,
                                        unique_fields=['product', 'store'],
                                        update_fields=[
                                            'product',
                                            'store',
                                            'initial_price',
                                            'promo_price',
                                            'discount']
                                        )
    logger.debug(LOG_ADD_TO_DB)
