import json
import logging
from datetime import datetime
from logging.config import dictConfig

from django.conf import settings

from parsing_stores.magnit.magnit_parsing import get_url
from products.models import ChainStore, Store, StoreLocation

dictConfig(settings.LOGGER_MAGNIT)
logger = logging.getLogger(f'root.{__name__}')

url_city = settings.PARSING_MAGNIT.get('URL_CITY')
url_stores = settings.PARSING_MAGNIT.get('URL_STORES')
headers = settings.PARSING_MAGNIT.get('HEADERS')
params_stores = settings.PARSING_MAGNIT.get('PARAMS_STORES')


def _parse_city_data(data):
    return {
        'region': data.get('region'),
        'city': data.get('city'),
        'latitude': str(data.get('latitude')),
        'longitude': str(data.get('longitude')),
    }


def get_cities():
    cities = get_url(url=url_city, headers=headers, params={}).get('cities')
    return [_parse_city_data(city) for city in cities]


def _parse_store_data(data, region, city):
    return {
        'chain_store': 'Магнит',
        'name': data.get('name'),
        'id_in_chain_store': data.get('id'),
        'region': region,
        'city': city,
        'address': ', '.join(data.get('address').split(', ')[1:]),
        'latitude': str(data.get('latitude')),
        'longitude': str(data.get('longitude')),
    }


def get_stores(cities):
    stores = []
    for city in cities:
        params_stores['latitude'] = city.get('latitude')
        params_stores['longitude'] = city.get('longitude')
        region = city.get('region')
        city_name = city.get('city')
        stores_in_city = get_url(url=url_stores, headers=headers, params=params_stores).get('stores')
        for store in stores_in_city:
            stores.append(_parse_store_data(store, region, city_name))
    with open('stores_magnit.json', 'w') as fl:
        fl.write(json.dumps(stores))
    return stores


def _split_store_data(store_data):
    store_location = {
        'region': store_data.pop('region'),
        'city': store_data.pop('city'),
        'address': store_data.pop('address'),
        'latitude': store_data.pop('latitude'),
        'longitude': store_data.pop('longitude'),
    }
    store_data['chain_store'] = ChainStore.objects.get(name=store_data.get('chain_store'))
    return store_data, store_location


def add_stores_in_db(stores):
    for store in stores:
        store_data, store_location = _split_store_data(store)
        if StoreLocation.objects.filter(**store_location).exists():
            st_location = StoreLocation.objects.filter(**store_location).first()
        else:
            st_location = StoreLocation.objects.create(**store_location)
            logger.info(f'Добавлен адрес магазина {st_location}')
        if not Store.objects.filter(location=st_location, **store_data).exists():
            Store.objects.create(location=st_location, **store_data)
            logger.info(f'Добавлен магазин <<{store_data}>> по адресу {st_location}')
        else:
            logger.info(f'Магазин <<{store_data}>> по адресу {st_location} уже есть в БД')


def main():
    start = datetime.today()
    logger.info('Начало получения данных магазинов "Магнит"')
    stores = get_stores(get_cities())
    add_stores_in_db(stores)
    logger.info(f'За время {datetime.today() - start} получены данные по {len(stores)} магазинам сети "Магнит"')
