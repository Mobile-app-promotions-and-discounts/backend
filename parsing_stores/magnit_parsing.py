# import json
# from pprint import pprint
# from time import sleep

import requests
from django.core.files.base import ContentFile

from parsing_stores.validators import check_product_magnit
from products.models import Category, Discount, Product, ProductsInStore, Store

url_products = 'https://web-gateway.middle-api.magnit.ru/v1/promotions'
url_stores = 'https://web-gateway.middle-api.magnit.ru/v1/cities'
headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Origin': 'https://magnit.ru',
    'Referer': 'https://magnit.ru/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  'Chrome/119.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'x-app-version': '0.1.0',
    'x-client-name': 'magnit',
    'x-device-id': 'v66jbingss',
    'x-device-platform': 'Web',
    'x-device-tag': 'disabled',
    'x-platform-version': 'window.navigator.userAgent',
}
params_products = {
    'offset': '0',
    'limit': '1',
    'storeId': '63452',
    'adult': 'true',
    'sortBy': 'priority',
    'order': 'desc',
}
params_stores = {
    'Limit': 1100,
    # 'query': 'Москва',
}


NO_DATA = -1

CATEGORIES = {
    'PRODUCTS': [
        'Хлеб и выпечка',
        'Овощи и фрукты',
        'Молоко, сыр, яйца',
        'Мясо, птица, колбасы',
        'Замороженные продукты',
        'Напитки',
        'Готовая еда',
        'Чай, кофе, какао',
        'Бакалея, соусы',
        'Кондитерские изделия',
        'Снеки, орехи',
        'Соусы и приправы',
        'Здоровое питание',
        'Рыба и морепродукты',
        'Готовая еда',
    ],
    'CLOTHES': [
        'Одежда и обувь',
    ],
    'HOME': [
        'Дом, сад',
        'Медтовары',
        'Бытовая техника',
        'Бытовая химия',
        'Скидки по карте',
        'Новинки',
        'Досуг',
        'Канцтовары',
        'Витамины и БАД',
        'Аксессуары',
        'Лекарства',
        'Печатная продукция',
    ],
    'COSMETICS': [
        'Косметика и парфюмерия',
        'Гигиена',
    ],
    'KIDS': [
        'Детям',
    ],
    'ZOO': [
        'Зоотовары',
    ],
    'AUTO:': ['Автотовары'],
    'HOLIDAYS': [
        'Алкоголь',
        'Новый год',
    ],
    'DIFFERENT': [
        'Скидки по карте',
        'Скидки на категории',
        '30% бонусами с подпиской',
        'Новинки',
        'Кешбек',
        'Разные категории',
        '0',
        'Проездные. Лотереи',
    ],
}


def get_url(url: str, params: dict, headers: dict) -> dict:
    """Получение данных с сайта."""
    response = requests.get(url=url, params=params, headers=headers)
    if response.status_code != 200:
        raise NotImplementedError(f'Адрес <<{url}>> недоступен')
    return response.json()


def _get_product_image(url):
    response = requests.get(url=url)
    if response.status_code != 200:
        raise NotImplementedError(f'Изображение по адресу <<{url}>> недоступно')
    return response.content


def split_product_data(product_data):
    """Разделить данные по данным моделей."""
    discount = product_data.pop('discount')
    price_in_store = product_data.pop('price_in_store')
    return product_data, discount, price_in_store


def _add_product(data, store=None):
    image_url = data.pop('image_url')
    image = _get_product_image(image_url)
    name_category = data.pop('category')
    category = ''
    if not Category.objects.all():
        raise ValueError('Категории товаров отсутствуют. Создайте категории товаров.')
    for key, value in CATEGORIES.items():
        if name_category in value and Category.objects.filter(name=key).exists():
            category = Category.objects.get(name=key)
    # print(name_category)
    # КОСТЫЛЬ. если нет такой категории товар попадает в разное.
    category = category if category else Category.objects.get(name='DIFFERENT')
    if not Product.objects.filter(category=category, **data).exists():
        return Product.objects.create(
            category=category,
            main_image=ContentFile(image, name='img.jpeg'),
            **data,
        )
    return Product.objects.get(
        category=category,
        **data,
    )


def _add_discount(data_discount):
    return Discount.objects.get_or_create(**data_discount)[0]


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
        product['discount']['discount_rate'] = item.get('discountPercentage', NO_DATA)
        product['price_in_store']['initial_price'] = str(item.get('oldPrice', NO_DATA))
        product['price_in_store']['promo_price'] = str(item.get('price', NO_DATA))
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
    for product in products:
        product_data, discount, price_in_store = split_product_data(product)
        price_in_store.pop('store_id')
        prod = _add_product(product_data)
        disc = _add_discount(discount)
        ProductsInStore.objects.get_or_create(
            product=prod,
            store=store,
            discount=disc,
            **price_in_store,
        )


def main():
    stores_id = [store.id_in_chain_store for store in Store.objects.all()]
    for store_id in stores_id:
        add_products_store_in_db(store_id)


if __name__ == '__main__':
    # pprint(main()[1][0])
    # pprint(read_data(get_url(url_products, params=params_products, headers=headers))[1])
    pass
