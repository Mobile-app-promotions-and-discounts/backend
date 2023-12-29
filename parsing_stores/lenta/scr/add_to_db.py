import logging

from django.core.files.base import ContentFile
from requests import Response

import parsing_stores.lenta.scr.config as cfg
from parsing_stores.lenta.scr.core import get_response
from products.models import (Category, ChainStore, Discount, Product,
                             ProductsInStore, Store, StoreLocation)

logger = logging.getLogger()


def add_category(category_data: dict) -> Category:
    """Подготовка картинки для db"""
    if not Category.objects.filter(name=category_data).exists():
        Category.objects.create(name=category_data)
    return Category.objects.get(name=category_data)


def add_image(url: str) -> bytes:
    """Подготовка картинки для db"""
    response: Response = get_response(
        options={'url': url, 'cookies': cfg.cookies, 'headers': cfg.HEADERS})
    return response.content


def add_store(store_data: dict) -> Store:
    """Подготовка магазина для db"""
    return Store.objects.create(
        name=store_data.get('name'),
        location=StoreLocation.objects.create(**store_data.get('location')),
        chain_store=ChainStore.objects.create(**store_data.get('chain_store'))
    )


def add_products(product_data: dict) -> Product:
    """Подготовка продукта для db"""
    category_data: str = product_data.pop('category')

    if product_data.get('main_image'):
        main_image: str = product_data.pop('main_image')[0]
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


def add_to_db(all_products_in_store: list, store_data: dict) -> None:
    """Заполнеиние БД ProductsInStore"""
    data = []
    for products_in_store in all_products_in_store:
        product_data: dict = products_in_store.pop('product')
        discount_data: dict = products_in_store.pop('discount')

        product: Product = add_products(product_data)
        store: Store = add_store(store_data)

        data.append(
            ProductsInStore(
                store=store,
                product=product,
                discount=Discount.objects.create(**discount_data),
                **products_in_store,
            )
        )
    ProductsInStore.objects.bulk_create(data)
