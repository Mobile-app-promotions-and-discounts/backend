import asyncio
from copy import deepcopy
from datetime import datetime
from logging import getLogger
from logging.config import dictConfig
from typing import List, Dict

from aiohttp import ClientSession

from parsing_stores.magnit.config import PARSING_MAGNIT
from products.models import Store


dictConfig(PARSING_MAGNIT.LOGGER_MAGNIT)
logger = getLogger(f'root.{__name__}')

request_settings = {
    'url': PARSING_MAGNIT.get('URL_PRODUCTS'),
    'headers': PARSING_MAGNIT.get('HEADERS'),
    'params': PARSING_MAGNIT.get('PARAMS_PRODUCTS')
}


async def get_data_in_url(session, request_setting):
    async with session.get(**request_setting) as result:
        return await result.json()


async def _get_image(session, url):
    async with session.get(url) as result:
        return await result.read()


def set_params(params, change_param, value_param):
    params[change_param] = value_param
    return params


def parse_data_product(data, data_keys):
    products = {}
    for out_key, in_key in data_keys:
        if 'category' in out_key:
            name_category = data.get(in_key)
            for key, value in PARSING_MAGNIT.get('CATEGORIES').items():
                if name_category in value:
                    products[out_key] = key
            if not products.get(out_key, False):
                products[out_key] = 'DIFFERENT'
        else:
            products[out_key] = data.get(in_key)
    return products


def get_image_name(st: str) -> str:
    """Извлечение названия картинки из url."""
    return st.split('?')[0].split('/')[-1]


async def get_product_in_stores(request_settings, ids_store):
    start = datetime.today()
    logger.info(f'Начало опроса {len(ids_store)} магазинов {start}')
    # store_param = PARSING_MAGNIT.get('PARAMS_PRODUCTS')
    async with ClientSession() as session:
        stores_params = []
        for id_store in ids_store:
            params = deepcopy(request_settings)
            params['params']['storeId'] = id_store
            stores_params.append(get_data_in_url(session, params))
        result = await asyncio.gather(*stores_params, return_exceptions=True)
    print(f'Время парсинга {datetime.today() - start}')
    return result


async def get_images(products: List[List[Dict[str, str | None]]]) -> List[bytes]:
    urls = [product.get('image_url') for product in products]
    async with ClientSession() as session:
        reqs = [_get_image(session, url) for url in urls]
        results = await asyncio.gather(*reqs, return_exceptions=True)
    for product, image in zip(products, results):
        product['image_name'] = get_image_name(product.pop('image_url'))
        if isinstance(image, Exception):
            product['image'] = None
        else:
            product['image'] = image
    return products


def run_get_data_in_stores():
    start = datetime.today()
    ids_store = [
        store[0] for store in Store.objects.filter(chain_store__name='Магнит').values_list('id_in_chain_store')
    ]
    result = asyncio.run(get_product_in_stores(request_settings=request_settings, ids_store=ids_store))
    r = []
    for products_store, store in zip(result, ids_store):
        if not isinstance(products_store, Exception):
            for product in products_store.get('data'):
                pr_data = parse_data_product(product, PARSING_MAGNIT.get('KEYS'))
                pr_data['id_in_chain_store'] = store
                r.append(pr_data)
        else:
            logger.info(f'Опрос магазина <{store}> завершился ошибкой <{products_store}>')
    products = asyncio.run(get_images(r))
    logger.info(f'Получено {len(r)} товаров')
    logger.info(f'Время работы {datetime.today() - start}')
    return products
