from time import sleep
import json
from pprint import pprint
import requests

from django.core.files.base import ContentFile

from products.models import Category, Discount, Product, ProductsInStore, Store
from parsing_stores.validators import check_product_magnit

# def check_product_magnit(product):
#     if requests.get(product['image_url']).status_code != 200:
#         return False
#     elif (
#         product['price_in_store']['initial_price'] <= 0 and
#         product['price_in_store']['promo_price'] <= 0
#     ):
#         return False
#     else:
#         return True

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
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
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
    'Limit': 1000000,
    # 'query': 'Москва',
}

test_data = {
    'barcode': '4600300088867',
    'category': 'Кондитерские изделия',
    'discount': {
        'discount_percentage': 50,
        'end_date': '2024-01-09',
        'old_price': 11999,
        'price': 5999,
        'start_date': '2023-12-20',
        'store': 'Магнит'
    },
    'image_url': 'https://promo-images.prod.ya.magnit.ru/media/promo/images/2400022587.png?response-content-type=image%2Fpng&AWSAccessKeyId=YCAJEHBIaXWYCFuHFkQb6rnPh&Signature=lsoQresnodcLRsOQTHjf2bAk2xs%3D&Expires=1703255633',
    'name': 'Шоколад АЛЁНКА молочный, 90г'
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
    ], # 'CLOTHES', 'Одежда и обувь'
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
    ], # 'Косметика и гигиена'
    'KIDS': [
        'Детям',
    ], # 'Для детей'
    'ZOO': [
        'Зоотовары',
    ], # 'Зоотовары'
    'AUTO:': ['Автотовары'], # 'Авто'
    'HOLIDAYS': [
        'Алкоголь',
        'Новый год',
    ], # 'К празднику'
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
    # discount = data.pop('discount')
    image_url = data.pop('image_url')
    image = _get_product_image(image_url)
    name_category = data.pop('category')
    category = ''
    if not Category.objects.all():
        raise ValueError('Категории товаров отсутствуют. Создайте категории товаров.')
    for key, value in CATEGORIES.items():
        if name_category in value and Category.objects.filter(name=key).exists():
            category = Category.objects.get(name=key)
    print(name_category)
    category = category if category else Category.objects.get(name='DIFFERENT')
    if not Product.objects.filter(category=category, **data).exists():
        return Product.objects.create(
            category=category,
            main_image=ContentFile(image, name='img.jpeg'),
            **data,
        )
    # else:
    return Product.objects.get(
        category=category,
        **data,
        )
    # return product


def _add_discount(data_discount):
    return Discount.objects.get_or_create(**data_discount)[0]


def read_data(request_data, store_id=None):
    """Извлечение данных товаров из данных запроса."""
    categories = []
    products = []
    # pprint(request_data.get('data')[0])
    for item in request_data.get('data'):
        # try:
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
        product['price_in_store']['initial_price'] = item.get('oldPrice', NO_DATA)
        product['price_in_store']['promo_price'] = item.get('price', NO_DATA)
        # print(check_product_magnit(product))
        if check_product_magnit(product):
            products.append(product)
        # except NotImplementedError:
        #     print(f'изображение <<{item.get("imageUrl")}>> не найдено')
        #     continue
    return categories, products


def add_products_store_in_db(id_in_chain_store):
    params_products['storeId'] = id_in_chain_store
    total_products = get_url(url_products, params=params_products, headers=headers).get('total')
    params_products['limit'] = total_products
    data = get_url(url_products, params=params_products, headers=headers)
    products = read_data(data)[1]
    store = Store.objects.get(id_in_chain_store=id_in_chain_store)
    # print(store)
    for product in products:
        # print(product)
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
