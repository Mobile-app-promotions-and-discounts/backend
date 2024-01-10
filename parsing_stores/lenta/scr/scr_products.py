import logging
from typing import List, Tuple

from requests import Response

import parsing_stores.lenta.scr.config as cfg
from parsing_stores.lenta.scr.core import get_response

logger = logging.getLogger()

LOG_FILTER_PRODUCTS_DISCOUNT = 'filter_products_discount - OK'
LOG_PRODUCTS_DISCOUNT = 'scr_products_discount - OK'
LOG_PRODUCTS_IN_STORE = 'get_products_in_store - OK'
LOG_PRODUCTS_ON_PAGE = 'get_products_on_page - OK'


def get_products_on_page(store_id: str, nodeCode: str, offset: int) -> Response:
    """
    Получить список продуктов в определеной категории и записать его в файл.
    'store' - словарь данных магазина
    'nodeCode' - параметр категории на сайте магазина
    """

    json_data: dict = {
        'nodeCode': nodeCode,
        'pageId': 'cc4fe51d-b4c0-4c96-be9b-ffebb9d67753',
        'filters': [],
        'typeSearch': 1,
        'sortingType': 'ByPriority',
        'offset': offset,
        'limit': cfg.PRODUCTS_ON_PAGE,
        'updateFilters': True,
    }
    requests_options: dict = {
        'url': cfg.URL_GET_PRODUCT.format(store_id),
        'cookies': cfg.COOKIES,
        'headers': cfg.HEADERS,
        'json': json_data
    }
    response: Response = get_response(options=requests_options,
                                      method='post')
    logger.debug(LOG_PRODUCTS_ON_PAGE)
    return response


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
            amount_products: int = 0
            while amount_products > 0 or offset == 0:
                product_page: List[dict] = get_products_on_page(
                    store.get('id_store'),
                    nodeCode,
                    offset
                ).json()
                if offset == 0:
                    amount_products: int = product_page.get('total')
                amount_products -= cfg.PRODUCTS_ON_PAGE
                if product_page and product_page != []:
                    product_page = product_page.get('skus')
                    prodacts_data: List[dict] = scr_products_discount(product_page, category_in_bd)
                    all_products_store.extend(prodacts_data)
                else:
                    break
                offset += cfg.PRODUCTS_ON_PAGE
    logger.debug(LOG_PRODUCTS_IN_STORE)
    return all_products_store, store
