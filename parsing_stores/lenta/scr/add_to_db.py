import logging
from typing import List

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
LOG_ADD_TO_DB = 'Из магазина c id {} добавлено в bd {} товаров'


@backoff.on_exception(backoff.expo, exception=[DatabaseError,], logger=logger)
def get_category_from_bd_or_create_new(category_data: str) -> Category:
    """Подготовка категории для db"""
    return Category.objects.get_or_create(name=category_data)[0]


@backoff.on_exception(backoff.expo, exception=[DatabaseError,], logger=logger)
def get_image(url: str) -> bytes:
    """Подготовка картинки для db"""
    response: Response = get_response(
        options={'url': url, 'cookies': cfg.COOKIES, 'headers': cfg.HEADERS})
    return response.content


@backoff.on_exception(backoff.expo, exception=[DatabaseError,], logger=logger)
def get_store_from_bd_or_create_new(store_data: dict) -> Store:
    """Подготовка магазина для db"""
    return Store.objects.get_or_create(
        name=store_data.get('name'),
        location=StoreLocation.objects.get_or_create(**store_data.get('location'))[0],
        chain_store=ChainStore.objects.get_or_create(**store_data.get('chain_store'))[0]
    )[0]


@backoff.on_exception(backoff.expo, exception=[DatabaseError,], logger=logger)
def get_product_from_bd_or_create_new(product_data: dict) -> Product:
    """Подготовка продукта для db"""
    category_data: str = product_data.pop('category', None)

    if product_data.get('main_image'):
        main_image: str = product_data.pop('main_image', None)[0]
        image: bytes = get_image(main_image)
        _image: ContentFile = ContentFile(image, name='img_product.jpeg')
    else:
        _image = None
    category: Category = get_category_from_bd_or_create_new(category_data)

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
def add_store_products_in_db(products_in_store: list, store_data: dict) -> None:
    """Заполнение БД ProductsInStore"""
    logger.debug(LOG_START_ADD_TO_DB)
    data = []
    store: Store = get_store_from_bd_or_create_new(store_data)
    for product in products_in_store:
        product_data: dict = product.pop('product', None)
        discount_data: dict = product.pop('discount', None)
        product_: Product = get_product_from_bd_or_create_new(product_data)
        data.append(
            ProductsInStore(
                store=store,
                product=product_,
                discount=Discount.objects.get_or_create(**discount_data)[0],
                **product,
            )
        )
    rez_list: List[ProductsInStore] = ProductsInStore.objects.bulk_create(
        data,
        ignore_conflicts=True
    )
    logger.debug(LOG_ADD_TO_DB.format(store_data.get('id_store'), len(rez_list)))
