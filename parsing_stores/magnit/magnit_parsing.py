import logging
from logging.config import dictConfig
import requests
from requests.exceptions import RequestException

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.exceptions import MultipleObjectsReturned

from parsing_stores.magnit.validators import check_product_magnit
from products.models import Category, Discount, Product, ProductsInStore, Store


dictConfig(settings.LOGGER_MAGNIT)
logger = logging.getLogger(f'root.{__name__}')

url_products = settings.PARSING_MAGNIT.get('URL_PRODUCTS')

headers = settings.PARSING_MAGNIT.get('HEADERS')
params_products = settings.PARSING_MAGNIT.get('PARAMS_PRODUCTS')
params_stores = settings.PARSING_MAGNIT.get('PARAMS_STORES')
no_data = settings.PARSING_MAGNIT.get('NO_DATA')
CATEGORIES = settings.PARSING_MAGNIT.get('CATEGORIES')


def get_url(url: str, params: dict, headers: dict) -> dict:
    """Получение данных с сайта."""
    response = requests.get(url=url, params=params, headers=headers)
    if response.status_code != 200:
        raise RequestException(f'Адрес <<{url}>> недоступен')
    return response.json()


def _get_product_image(url):
    response = requests.get(url=url)
    if response.status_code != 200:
        raise RequestException(f'Изображение по адресу <<{url}>> недоступно')
    return response.content


def split_product_data(product_data):
    """Разделить данные по данным моделей."""
    discount = product_data.pop('discount')
    price_in_store = product_data.pop('price_in_store')
    return product_data, discount, price_in_store


def _add_product(data, store=None):
    image_url = data.pop('image_url')
    try:
        image = _get_product_image(image_url)
    except RequestException as exc:
        logger.exception(msg=exc)
    name_category = data.pop('category')
    category = ''
    if not Category.objects.all():
        raise ValueError('Категории товаров отсутствуют. Создайте категории товаров.')
    for key, value in CATEGORIES.items():
        if name_category in value and Category.objects.filter(name=key).exists():
            category = Category.objects.get(name=key)
    # КОСТЫЛЬ. если нет такой категории товар попадает в разное.
    category = category if category else Category.objects.get(name='DIFFERENT')
    if not Product.objects.filter(**data).exists():
        logger.info(f'Добавление продукта в категорию <<{category}>> с данными <<{data}>> в БД')
        return Product.objects.create(
            category=category,
            main_image=ContentFile(image, name='img.jpeg'),
            **data,
        )
    logger.info(f'Извлечение продукта с данными <<{data}>> из БД')
    return Product.objects.get(**data)


def _add_discount(data_discount):
    try:
        if not Discount.objects.filter(**data_discount).exists():
            logger.info(msg=f'Добавление акции с данными <<{data_discount}>>')
            return Discount.objects.create(**data_discount)
        logger.info(msg=f'Извлечение акции с данными <<{data_discount}>> из БД')
        return Discount.objects.get(**data_discount)
    except MultipleObjectsReturned as exc:
        logger.exception(exc)
        return Discount.objects.filter(**data_discount).first()


def read_data(request_data, store_id=None):
    """Извлечение данных товаров из данных запроса."""
    categories = []
    products = []
    for item in request_data.get('data'):
        product = {
            'price_in_store': {'store_id': 'Магнит ' + str(store_id)},
            'discount': {},
        }
        product['name'] = item.get('name')
        product['barcode'] = item.get('barcode')
        product['image_url'] = item.get('imageUrl')
        category = item.get('categoryName')
        if category not in categories:
            categories.append(category)
        product['category'] = category
        product['discount']['discount_unit'] = '%'
        product['discount']['discount_start'] = item.get('startDate')
        product['discount']['discount_end'] = item.get('endDate')
        product['discount']['discount_rate'] = item.get('discountPercentage', no_data)
        product['price_in_store']['initial_price'] = str(item.get('oldPrice', no_data))
        product['price_in_store']['promo_price'] = str(item.get('price', no_data))
        if check_product_magnit(product):
            products.append(product)
    return categories, products


def add_products_store_in_db(id_in_chain_store):
    params_products['storeId'] = id_in_chain_store
    total_products = get_url(url_products, params=params_products, headers=headers).get('total')
    params_products['limit'] = total_products
    data = get_url(url_products, params=params_products, headers=headers)
    products = read_data(data)[1]
    store = Store.objects.get(id_in_chain_store=id_in_chain_store)
    logger.info(f'товары по магазину <<{store}>> получены')
    for product in products:
        product_data, discount, price_in_store = split_product_data(product)
        price_in_store.pop('store_id')
        prod = _add_product(product_data)
        disc = _add_discount(discount)
        if not ProductsInStore.objects.filter(product=prod, store=store).exists():
            ProductsInStore.objects.create(
                product=prod,
                store=store,
                discount=disc,
                **price_in_store,
            )
            logger.info(msg=f'Товар {prod} добавлен в магазин {store}')


def main():
    stores_id = [store.id_in_chain_store for store in Store.objects.filter(chain_store__name='Магнит')]
    for store_id in stores_id:
        try:
            add_products_store_in_db(store_id)
        except RequestException as exc:
            logger.exception(exc)
            continue


if __name__ == '__main__':
    # pprint(main()[1][0])
    # pprint(read_data(get_url(url_products, params=params_products, headers=headers))[1])
    pass
