import logging
from typing import List

import parsing_stores.lenta.scr.config as cfg
from parsing_stores.lenta.scr.core import (get_response, open_json_file,
                                           save_json_file)

logger = logging.getLogger()

SCR_STORE = 'Спарсено {} магазинов в городе {}.'


def get_and_save_all_stores() -> None:
    """Получить список магазинов сети и записать его в файл."""

    requests_options: dict = {'url': cfg.URL_GET_STORES,
                              'cookies': cfg.COOKIES,
                              'headers': cfg.HEADERS}

    response_json = get_response(options=requests_options).json()
    save_json_file(response_json, cfg.FILE_NAME['ALL_STORES'])


def get_and_save_stores_in_city(city: str) -> None:
    """
    Получить список магазинов в городе -'city'

    Пример значение {модель - сайт}
    {
    'id': '0067',
    'city_key': 'msk',
    'name': 'Лента',
    'city': 'Москва и МО',
    'street': 'ул. 9-я Парковая, д. 68, корп. 5',
    'latitude': 54.907765,
    'longitude': 52.255366,
    }
    """

    all_stores: List[dict] = open_json_file(cfg.FILE_NAME['ALL_STORES'])
    stores_in_city: List[dict] = []

    stores_city_list: List[dict] = list(
        filter(lambda d: d['cityName'].split()[0] == city, all_stores)
    )
    for store in stores_city_list:
        data: dict = {
            'id_store': store.get('id'),
            'name': cfg.NAME_STORE,
            'location': {
                'region': store.get('cityName'),
                'city': store.get('cityName').split()[0].strip(),
                'address': store.get('address'),
                'latitude': str(store.get('lat')),
                'longitude': str(store.get('long')),
            },
            'chain_store': {
                'name': cfg.NAME_STORE,
            },
        }
        stores_in_city.append(data)
    logger.debug(SCR_STORE.format(len(stores_in_city), city))
    save_json_file(
        stores_in_city,
        cfg.FILE_NAME['STORES_IN_SITY'].format(city)
    )
