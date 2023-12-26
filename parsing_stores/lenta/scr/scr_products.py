import logging

import scr.config as cfg
import scr.msg as msg
from scr.core import (get_response,
                      save_json_file,
                      open_json_file)


logger = logging.getLogger()


def get_products_category_page(store, nodeCode, offset):
    """
    Получить список продуктов в определеной категории и записать его в файл.
    'store' - словарь данных магазина
    'nodeCode' - параметр категории на сайте магазина

    """

    while True:
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
            'url': cfg.URL_GET_PRODACT.format(store.get('id_store')),
            'cookies': cfg.cookies,
            'headers': cfg.HEADERS,
            'json': json_data
        }
        response = get_response(options=requests_options,
                                metod='post').json().get('skus')
        return response


def filter_products_discount(name_cat_bd, offset):
    """
    'store' - словарь данных магазина
    'nodeCode' - параметр категории на сайте магазина
    'name_cat_bd' - имя категории в БД

    """


def get_products_in_store(store):
    """
    Получить список продуктов для магазина.
    """

    prodacts_data = []

    for name_cat_bd, nodeCode_list in cfg.CATEGORY.items():
        for nodeCode in nodeCode_list:
            if not nodeCode:
                continue
            offset = 0
            while True:
                product_page = get_products_category_page(
                    store,
                    nodeCode,
                    offset
                )
                if product_page:
                    save_json_file(
                        product_page,
                        cfg.FILE_NAME['PRODUCTS_IN_CATEGORY'].format(name_cat_bd)
                    )
                response_prodact = open_json_file(
                    cfg.FILE_NAME['PRODUCTS_IN_CATEGORY'].format(name_cat_bd)
                )
                for value in response_prodact:
                    if not value.get('promoId'):
                        break
                    products_in_store = {
                        'product': {
                            'name': value.get('title'),
                            'description': (value.get('description')
                                            .replace('\r', '').replace('\n', '')),
                            'barcode': value.get('code'),
                            'category': name_cat_bd,
                        },
                        'base_price': int(value.get('regularPrice')*100),
                        'sale_price': int(value.get('discountPrice')*100),
                        'discount': {
                            'discount_rate': value.get('offerDescription')[1:-1],
                            'discount_start': value.get('validityStartDate')[:10],
                            'discount_end': value.get('validityEndDate')[:10],
                            'discount_card': cfg.LENTA_VALUE
                        }
                    }
                    if value.get('image'):
                        products_in_store['product']['main_image'] = [
                                value.get('image').get('fullSize'),
                                *[i.get('fullSize') for i in value.get('images')]
                            ]
                    else:
                        products_in_store['product']['main_image'] = None
                    prodacts_data.append(products_in_store)
                else:
                    break
                offset = offset + cfg.PRODUCTS_ON_PAGE
            save_json_file(prodacts_data, f'products_ФТВ{name_cat_bd}')
    logger.debug(msg.SCR_PRODUCTS.format(
        len(prodacts_data),
        store.get('id_store')
    ))
    return prodacts_data
