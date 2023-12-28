import logging

import parsing_stores.lenta.scr.config as cfg
from parsing_stores.lenta.scr.core import get_response


logger = logging.getLogger()


def get_products_on_page(store_id, nodeCode, offset):
    """
    Получить список продуктов в определеной категории и записать его в файл.
    'store' - словарь данных магазина
    'nodeCode' - параметр категории на сайте магазина
    """

    json_data = {
        'nodeCode': nodeCode,
        'filters': [],
        'typeSearch': 1,
        'sortingType': 'ByPriority',
        'offset': offset,
        'limit': cfg.PRODUCTS_ON_PAGE,
        'updateFilters': True,
    }
    requests_options = {
        'url': cfg.URL_GET_PRODACT.format(store_id),
        'cookies': cfg.cookies,
        'headers': cfg.HEADERS,
        'json': json_data
    }
    response = get_response(options=requests_options,
                            metod='post')
    logger.debug('get_products_on_page - OK')
    return response


def filter_products_discount(product_page):
    """Отфильтровать товары со скидками."""
    products_discount = list(
        filter(lambda d: d['regularPrice'] != d['discountPrice'], product_page)
    )
    logger.debug('filter_products_discount - OK')
    return products_discount


def scr_products_discount(products_discount, name_cat_bd):
    """Получить необходимые данные продуктов."""
    prodacts_data = []

    for value in products_discount:
        products_in_store = {
            'product': {
                'name': value.get('title'),
                'description': (value.get('description')
                                .replace('\r', '').replace('\n', '')),
                'barcode': value.get('code'),
                'category': name_cat_bd,
            },
            'initial_price': str(value.get('regularPrice')).replace('.', ''),
            'promo_price': str(value.get('discountPrice')).replace('.', ''),
            'discount': {
                'discount_rate': value.get('promoPercent'),
                'discount_start': value.get('validityStartDate')[:10],
                'discount_end': value.get('validityEndDate')[:10],
                'discount_card': cfg.LENTA_VALUE
            }
        }
        if value.get('image'):
            products_in_store['product']['main_image'] = [
                value.get('image').get('thumbnail'),
                *[i.get('thumbnail') for i in value.get('images')]
            ]
        prodacts_data.append(products_in_store)
    logger.debug('scr_products_discount - OK')
    return prodacts_data


def get_products_in_store(store):
    """
    Получить список продуктов для магазина.
    """
    all_products_store = []

    for name_cat_bd, nodeCode_list in cfg.CATEGORY.items():
        for nodeCode in nodeCode_list:
            if not nodeCode:
                continue
            offset = 0

            while True:
                product_page = get_products_on_page(
                    store.get('id_store'),
                    nodeCode,
                    offset
                ).json().get('skus')
                if product_page and len(product_page) != 0:
                    products_discount = filter_products_discount(product_page)
                    prodacts_data = scr_products_discount(products_discount, name_cat_bd)
                    all_products_store.extend(prodacts_data)
                else:
                    break
                offset += cfg.PRODUCTS_ON_PAGE
    return all_products_store, store
