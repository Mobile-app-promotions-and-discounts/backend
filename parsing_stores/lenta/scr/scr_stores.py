import logging

import scr.config as cfg
import scr.msg as msg
from scr.core import (get_response,
                      save_json_file,
                      open_json_file)


logger = logging.getLogger()


def get_and_save_all_stores():
    """Получить список магазинов сети и записать его в файл."""

    requests_options = {'url': cfg.URL_GET_STORES,
                        'cookies': cfg.cookies,
                        'headers': cfg.HEADERS}

    response_json = get_response(options=requests_options).json()
    save_json_file(response_json, cfg.FILE_NAME['ALL_STORES'])


def get_stores_in_city(city):
    """
    Получить список магазинов в городе -'city'

    Пример значение {модель - сайт}
    {
    'id': '0067',
    'city_key': 'msk',
    'name': 'Лента',
    'city': 'Москва и МО',
    'street': 'ул. 9-я Парковая, д. 68, корп. 5',
    'lat': 54.907765,
    'long': 52.255366,
    }
    """

    all_stores = open_json_file(cfg.FILE_NAME['ALL_STORES'])
    stores_in_city = []

    stores_city_list = list(
        filter(lambda d: d['cityName'].split()[0] == city, all_stores)
    )
    for store in stores_city_list:
        data = {
            'id_store': store.get('id'),
            'name': cfg.NAME_STORE,
            'location': {
                'region': store.get('cityName'),
                'city': store.get('cityName').split()[0].strip(),
                'address': store.get('address'),
                'lat': store.get('lat'),
                'long': store.get('long'),
            },
            'chain_store': {
                'name': cfg.NAME_STORE,
            },
        }
        stores_in_city.append(data)
    logger.debug(msg.SCR_STORE.format(len(stores_in_city), city))
    return stores_in_city
