import aiohttp
import json
import logging
from typing import Any


import backoff
import requests
from requests import Response

import parsing_stores.lenta.scr.config as cfg

logger = logging.getLogger()

ALL_STORES_NOT_FOUND = 'Файл {} не найден.'
RESPONSE_STATUS = 'Response - Status code {}'
REQUEST_ERROR = 'Запрос {} - {}'
REQUEST_START = 'Запрос {}'


@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException,
                      max_time=60,
                      logger=logger)
def get_response(options: dict = None, method: str = 'get') -> Response:
    """Функция выполняет request и возвращает response"""
    logger.debug(REQUEST_START.format(options.get('url')))
    response: Response = (requests.get(**options)
                          if method == 'get'
                          else requests.post(**options))
    response.raise_for_status()
    if response.status_code == requests.codes.ok:
        logger.debug(RESPONSE_STATUS.format(
            response.status_code,
            options.get('url')))
    else:
        logger.error(RESPONSE_STATUS.format(response.status_code))
    return response


@backoff.on_exception(backoff.expo,
                      aiohttp.ClientError,
                      max_time=60,
                      logger=logger)
async def aget_response(options: dict = None,
                        method: str = 'get',
                        return_: str = 'json') -> Any:
    """Функция асинхронно выполняет request и возвращает response"""
    async with aiohttp.ClientSession(cookies=cfg.COOKIES, headers=cfg.HEADERS) as session:
        logger.debug(REQUEST_START.format(options.get('url')))
        async with session.request(method=method, **options) as resp:
            if return_ == 'content':
                return await resp.read()
            return await resp.json()


def save_json_file(file_: Any, name_file: str, mode: str = 'w') -> None:
    """Записать файл json c именем 'name_file'."""
    with open(cfg.PATH_FILE.format(name_file), mode, encoding='utf-8') as file:
        json.dump(file_, file, indent=4, ensure_ascii=False)
        file.write('\n')


def open_json_file(name_file: str) -> Any:
    """
    Открывает и возвращает файл
      'PATH_FILE'- путь к файлу в виде строки
    """
    try:
        with open(cfg.PATH_FILE.format(name_file), encoding='utf-8') as file:
            file = file.read()
        return json.loads(file)
    except FileNotFoundError:
        logger.exception(ALL_STORES_NOT_FOUND.format(name_file))
