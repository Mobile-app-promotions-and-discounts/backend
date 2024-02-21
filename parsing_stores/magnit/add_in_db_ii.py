# Второй вариант с bulk_create
# ранняя проверка на отсутствие цены
from logging import getLogger
from logging.config import dictConfig

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404

from parsing_stores.magnit.async_magnit_parsing import run_get_data_in_stores
from parsing_stores.magnit.config import LOGGER_MAGNIT
from parsing_stores.magnit.decorators import calc_time_work
from parsing_stores.magnit.utils import (get_discount_data, get_product_data,
                                         is_duplicate_in_store_ii,
                                         is_duplicate_product)
from products.models import Category, Discount, Product, ProductsInStore, Store

dictConfig(LOGGER_MAGNIT)
logger = getLogger(f'root.{__name__}')


def sort_data(data):
    """Отсеиваю товары без цены и дубли продуктов и акций."""
    products_data = []
    discounts_data = []
    products_in_stores_data = []
    for item in data:
        if item.get('initial_price') or item.get('promo_price'):
            if not is_duplicate_product(item, products_data):
                products_data.append(get_product_data(item))
                logger.debug(f'Добавлен продукт с именем {item.get("name")}')
            else:
                logger.debug(f'Найден дубликат продукта с именем {item.get("name")}')
            discount = get_discount_data(item)
            if discount not in discounts_data:
                discounts_data.append(discount)
            if not is_duplicate_in_store_ii(item, products_in_stores_data):
                products_in_stores_data.append(item)
                logger.debug(f'В магазин {item.get("id_in_chain_store")} добавлен продукт {item.get("name")}')
            else:
                logger.debug('Найден продукт дублирующийся в магазине')
    return products_data, discounts_data, products_in_stores_data


def create_product_obj(product_data):
    """Создание объекта продукта из данных продукта."""
    try:
        category = Category.objects.get(name=product_data.pop('category'))
        image = ContentFile(
            product_data.pop('image'),
            name=product_data.pop('image_name'),
        )
    except Exception as exc:
        logger.exception(exc)
    return Product(
        category=category,
        main_image=image,
        **product_data,

    )


def create_discount_obj(discount_data):
    return Discount(**discount_data)


def create_product_in_store_obj(product_in_store_data):
    try:
        product = get_object_or_404(Product, name=product_in_store_data.get('name'))
        store = get_object_or_404(Store, id_in_chain_store=product_in_store_data.get('id_in_chain_store'))
        discount = get_object_or_404(Discount, **get_discount_data(product_in_store_data))
    except Exception as exc:
        logger.exception(exc)
    return ProductsInStore(
        product=product,
        store=store,
        discount=discount,
        # Убрать 2 заглушки отсутствия цены на этапе проверки полученных данных
        initial_price=product_in_store_data.get('initial_price') if product_in_store_data.get('initial_price') else '',
        promo_price=product_in_store_data.get('promo_price') if product_in_store_data.get('promo_price') else '',
    )


@calc_time_work
def run_add_data_in_db():
    data = run_get_data_in_stores()
    products, discounts, products_in_stores = sort_data(data)
    add_products = Product.objects.bulk_create(
        [create_product_obj(pr_data) for pr_data in products],
        ignore_conflicts=True,
    )
    add_discounts = Discount.objects.bulk_create(
        [create_discount_obj(ds_data) for ds_data in discounts],
        ignore_conflicts=True,
    )
    add_products_in_stores = ProductsInStore.objects.bulk_create(
        [create_product_in_store_obj(pr_in_store_data) for pr_in_store_data in products_in_stores],
        update_conflicts=True,
        update_fields=['initial_price', 'promo_price'],
        unique_fields=['product', 'store'],
    )
    logger.info(
        f'Добавлено: продуктов- {len(add_products)}; '
        f'акций- {len(add_discounts)}; '
        f'продуктов в магазин- {len(add_products_in_stores)}'
    )
    return add_products, add_discounts, add_products_in_stores
