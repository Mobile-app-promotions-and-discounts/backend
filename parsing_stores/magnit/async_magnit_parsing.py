import json
import asyncio
from copy import deepcopy
from datetime import datetime
from typing import List, Dict

from aiohttp import ClientSession

from parsing_stores.magnit.config import PARSING_MAGNIT
from products.models import Store


ids_store = ['61485', '61783', '120485', '167002', '100372', '7818', '92465', '168924', '127462', '104572', '124104', '201258', '247011', '61726', '202930', '177815', '266606', '61785', '61010', '14809', '59202', '14845', '94738', '253131', '6', '53085', '188360', '123071', '193219', '1036']
# ids_store = ['61485', '120485', '167002', '168924', '127462', '104572', '124104', '201258', '247011', '61726', '202930', '177815', '266606', '61785', '61010', '14809', '59202', '94738', '253131', '53085', '188360', '123071', '1036']
# ids_store = ['127462', '6157', '63452']
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
        print('Начало запроса')
        return await result.read()


def set_params(params, change_param, value_param):
    params[change_param] = value_param
    return params


def parse_data_product(data, data_keys):
    discount = {}
    product = {}
    price = {}
    for out_key, in_key in data_keys:
        if 'discount' in out_key:
            discount[out_key] = data.get(in_key)
        elif 'price' in out_key:
            price[out_key] = data.get(in_key)
        elif 'category' in out_key:
            name_category = data.get(in_key)
            for key, value in PARSING_MAGNIT.get('CATEGORIES').items():
                if name_category in value:
                    product[out_key] = key
            if not product.get(out_key, False):
                product[out_key] = 'DIFFERENT'
        else:
            product[out_key] = data.get(in_key)
    return [product, discount, price]


def get_image_name(st: str) -> str:
    """Извлечение названия картинки из url."""
    return st.split('?')[0].split('/')[-1]


async def get_product_in_stores(request_settings, ids_store):
    start = datetime.today()
    print(f'Начало опроса {len(ids_store)} магазинов {start}')
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
    urls = [product[0].get('image_url') for product in products]
    async with ClientSession() as session:
        reqs = [_get_image(session, url) for url in urls]
        results = await asyncio.gather(*reqs, return_exceptions=True)
    for product, image in zip(products, results):
        if isinstance(image, Exception):
            product[0]['image'] = None
        else:
            product[0]['image'] = image
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
            # r[store] = [parse_data_product(d, PARSING_MAGNIT.get('KEYS')) for d in products_store.get('data')]
            for product in products_store.get('data'):
                pr_data = parse_data_product(product, PARSING_MAGNIT.get('KEYS'))
                pr_data.append(dict(id_in_chain_store=store))
                r.append(pr_data)
    products = asyncio.run(get_images(r))
    print(f'Опрошено {len(r)} магазинов')
    print(datetime.today() - start)
    # with open('products_in_magnit.json', 'w') as file:
    #     file.write(json.dumps(r))
    print(f'Время работы {datetime.today() - start}')
    return products
# pprint(asyncio.run(main()))
