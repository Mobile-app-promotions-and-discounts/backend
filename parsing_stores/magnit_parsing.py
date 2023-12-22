from time import sleep
import json
from pprint import pprint
import requests

from django.core.files.base import ContentFile

from products.models import Category, Discount, Product, ProductsInStore


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

params = {
    'offset': '0',
    'limit': '1',
    'storeId': '88871',
    'adult': 'true',
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
    ],
    'CLOTHES': [], # 'CLOTHES', 'Одежда и обувь'
    'HOME': [
        'Дом, сад',
        'Медтовары',
        'Бытовая техника',
        'Бытовая химия',
        'Скидки по карте',
        'Новинки',
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
    'AUTO:': [], # 'Авто'
    'HOLIDAYS': [
        'Алкоголь',
    ], # 'К празднику'
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


def add_product(data, store=None):
    # discount = data.pop('discount')
    image_url = data.pop('image_url')
    image = _get_product_image(image_url)
    name_category = data.pop('category')
    if not Category.objects.all():
        raise ValueError('Категории товаров отсутствуют. Создайте категории товаров.')
    for key, value in CATEGORIES.items():
        if name_category in value and Category.objects.filter(name=key).exists():
            category = Category.objects.get(name=key)
            if not Product.objects.filter(
                category=category,
                main_image=ContentFile(image, name='img.jpeg'),
                **data,
            ).exists():
                Product.objects.create(
                    category=category,
                    main_image=ContentFile(image, name='img.jpeg'),
                    **data,
                )
                break
        # Product.objects.create(main_image=image, **data)


def _add_discount(data_discount):
    return Discount.objects.get_or_create(**data_discount)


def read_data(request_data, store_id=None):
    """Извлечение данных товаров из данных запроса."""
    categories = []
    products = []
    # pprint(request_data.get('data')[0])
    for item in request_data.get('data'):
        product = {'price_in_store': {'store_id': 'Магнит ' + str(store_id)}}
        product['discount'] = {}
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
        product['discount']['discount_rate'] = item.get('discountPercentage')
        product['price_in_store']['initial_price'] = item.get('oldPrice')
        product['price_in_store']['promo_price'] = item.get('price')
        products.append(product)
    return categories, products


def main():
    total_products = get_url(url_chain_store, params=params, headers=headers).get('total')
    params['limit'] = total_products
    data = get_url(url_chain_store, params=params, headers=headers)
    # categories, products = read_data(data)
    return read_data(data)

    # with open('categories_data.json', 'w') as file:
    #     file.write(json.dumps(categories, sort_keys=True, indent=4))

    # with open('products_data.json', 'w') as file:
    #     file.write(json.dumps(products, sort_keys=True, indent=4))

    # pprint(categories)
    # pprint(products[0])
    # pprint(products[-1])
    # print(len(products))


# add_product(test_data)

if __name__ == '__main__':


    url_chain_store = 'https://web-gateway.middle-api.magnit.ru/v1/promotions'

    pprint(main()[1][0])
