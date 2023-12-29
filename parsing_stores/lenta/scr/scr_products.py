import logging
from typing import List, Tuple

from requests import Response

import parsing_stores.lenta.scr.config as cfg
from parsing_stores.lenta.scr.core import get_response

logger = logging.getLogger()

LOG_PRODUCTS_ON_PAGE = 'get_products_on_page - OK'
LOG_FILTER_PRODUCTS_DISCOUNT = 'filter_products_discount - OK'
LOG_PRODUCTS_DISCOUNT = 'scr_products_discount - OK'


def get_products_on_page(store_id: str, nodeCode: str, offset: int) -> Response:
    """
    Получить список продуктов в определеной категории и записать его в файл.
    'store' - словарь данных магазина
    'nodeCode' - параметр категории на сайте магазина
    """

    json_data: dict = {
        'nodeCode': nodeCode,
        'filters': [],
        'typeSearch': 1,
        'sortingType': 'ByPriority',
        'offset': offset,
        'limit': cfg.PRODUCTS_ON_PAGE,
        'updateFilters': True,
    }
    requests_options: dict = {
        'url': cfg.URL_GET_PRODUCT.format(store_id),
        'cookies': cfg.cookies,
        'headers': cfg.HEADERS,
        'json': json_data
    }
    response: Response = get_response(options=requests_options,
                                      method='post')
    logger.debug(LOG_PRODUCTS_ON_PAGE)
    return response


def filter_products_discount(product_page: List[dict]) -> List[dict]:
    """Отфильтровать товары со скидками."""
    products_discount: List[dict] = list(
        filter(lambda d: d['regularPrice'] != d['discountPrice'], product_page)
    )
    logger.debug(LOG_FILTER_PRODUCTS_DISCOUNT)
    return products_discount


def scr_products_discount(products_discount: List[dict], category_in_bd: str) -> List[dict]:
    """Получить необходимые данные продуктов."""
    products_data = []

    for value in products_discount:
        products_in_store: dict = {
            'product': {
                'name': value.get('title'),
                'description': (value.get('description')
                                .replace('\r', '').replace('\n', '')),
                'barcode': value.get('code'),
                'category': category_in_bd,
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
        products_data.append(products_in_store)
    logger.debug(LOG_PRODUCTS_DISCOUNT)
    return products_data


def get_products_in_store(store: dict) -> Tuple[list, dict]:
    """
    Получить список продуктов для магазина.
    """
    all_products_store = []

    for category_in_bd, nodeCode_list in cfg.CATEGORY.items():
        for nodeCode in nodeCode_list:
            if not nodeCode:
                continue
            offset: int = 0

            while True:
                product_page: List[dict] = get_products_on_page(
                    store.get('id_store'),
                    nodeCode,
                    offset
                ).json().get('skus')
                if product_page and len(product_page) != 0:
                    products_discount: List[dict] = filter_products_discount(product_page)
                    prodacts_data: List[dict] = scr_products_discount(products_discount, category_in_bd)
                    all_products_store.extend(prodacts_data)
                else:
                    break
                offset += cfg.PRODUCTS_ON_PAGE
    return all_products_store, store
