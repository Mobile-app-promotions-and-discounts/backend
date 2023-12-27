import json
import logging
import requests
import time

import scr.config as cfg
import scr.msg as msg

logger = logging.getLogger()


def get_response(options=None, metod='get'):
    logger.debug(msg.REQUEST_START.format(options.get('url')))
    try:
        response = (requests.get(**options)
                    if metod == 'get'
                    else requests.post(**options))
        response.raise_for_status()
        if response.status_code == requests.codes.ok:
            logger.debug(msg.RESPONSE_STATUS.format(
                response.status_code,
                options.get('url')))
        logger.error(msg.RESPONSE_STATUS.format(response.status_code))
    except requests.RequestException as error:
        logger.error(msg.REQUEST_ERROR.format(options.get('url'), error))
        time.sleep(5)
        response = get_response(options, metod)
    return response


def save_json_file(file_, name_file, mode='w', newline='\n'):
    """Записать файл json c именем 'name_file'."""
    with open(cfg.PATH_FILE.format(name_file), mode, encoding='utf-8') as file:
        json.dump(file_, file, indent=4, ensure_ascii=False)
        file.write('\n')


def open_json_file(name_file):
    """
    Открывает и возвращает файл
      'path_file'- путь к файлу в виде строки
    """
    try:
        with open(cfg.PATH_FILE.format(name_file), encoding='utf-8') as file:
            file = file.read()
        return json.loads(file)
    except FileNotFoundError:
        logger.exception(msg.ALL_STORES_NOT_FOUND.format(name_file))
