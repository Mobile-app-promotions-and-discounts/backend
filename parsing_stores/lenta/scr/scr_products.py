import logging
from typing import List, Tuple

from requests import Response

import parsing_stores.lenta.scr.config as cfg
from parsing_stores.lenta.scr.core import aget_response

logger = logging.getLogger()

LOG_FILTER_PRODUCTS_DISCOUNT = 'filter_products_discount - OK'
LOG_PRODUCTS_DISCOUNT = 'scr_products_discount - OK'
LOG_PRODUCTS_IN_STORE = 'Из магазина c id {} спарсено {} товаров'
LOG_PRODUCTS_ON_PAGE = 'get_products_on_page - OK'


async def aget_products_on_page(store_id: str, node_code: str, offset: int) -> Response:
    """
    Получить список продуктов в определеной категории.
    'store_id' - id магазина на сайте
    'nodeCode' - параметр категории на сайте магазина
    'offset' - параметр пагинации.
    PAGE_ID - параметр запроса(получения только товаров со скидкой)
    """

    json_data: dict = {
        'nodeCode': node_code,
        'pageId': cfg.PAGE_ID,
        'filters': [],
        'typeSearch': 1,
        'sortingType': 'ByPriority',
        'offset': offset,
        'limit': cfg.PRODUCTS_ON_PAGE,
        'updateFilters': True,
    }
    requests_options: dict = {
        'url': cfg.URL_GET_PRODUCT.format(store_id),
        'json': json_data
    }
    response_json: Response = await aget_response(method='post',
                                                  options=requests_options)
    logger.debug(LOG_PRODUCTS_ON_PAGE)
    return response_json


async def aget_image(url: str) -> bytes:
    """Подготовка картинки для db"""
    response: bytes = await aget_response(
        options={'url': url}, return_='content')
    return response


async def ascr_products_discount(products_discount: List[dict], category_in_bd: str) -> List[dict]:
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
                await aget_image(value.get('image').get('thumbnail')),
                *[i.get('thumbnail') for i in value.get('images')]
            ]
        products_data.append(products_in_store)
    logger.debug(LOG_PRODUCTS_DISCOUNT)
    return products_data


async def aget_products_in_store(store: dict) -> Tuple[list, dict]:
    """
    Получить список продуктов для магазина.
    """
    all_products_store = []

    for category_in_bd, node_code_list in cfg.CATEGORY.items():
        for node_code in node_code_list:
            if not node_code:
                continue
            offset: int = 0
            amount_products: int = 0
            while amount_products > 0 or offset == 0:
                product_page: List[dict] = await aget_products_on_page(
                    store.get('id_store'),
                    node_code,
                    offset
                )
                if offset == 0:
                    amount_products: int = product_page.get('total')
                amount_products -= cfg.PRODUCTS_ON_PAGE
                if product_page:
                    product_page = product_page.get('skus')
                    prodacts_data: List[dict] = await ascr_products_discount(product_page, category_in_bd)
                    all_products_store.extend(prodacts_data)
                else:
                    break
                offset += cfg.PRODUCTS_ON_PAGE
    logger.debug(LOG_PRODUCTS_IN_STORE.format(store.get('id_store'), len(all_products_store)))
    return all_products_store, store
