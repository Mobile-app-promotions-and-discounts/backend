import logging
import sys
# from logging.config import fileConfig

import scr.config as cfg
from scr.core import save_json_file
from scr.scr_products import get_products_in_store
from scr.scr_stores import (get_and_save_all_stores,
                            get_stores_in_city)


# fileConfig('logging.ini')
logger = logging.getLogger()


def main():
    get_and_save_all_stores()
    try:
        for city in cfg.CITY_APPLICATIONS:
            stores_in_city = get_stores_in_city(city)
            save_json_file(
                stores_in_city,
                cfg.FILE_NAME['STORES_IN_SITY'].format(city)
            )
            for store in stores_in_city:
                get_products_in_store(store)
                # save_json_file(
                #     products,
                #     cfg.FILE_NAME['PRODUCTS_IN_STORE'].format(store.get('id'))
                # )
                # with open(
                #     f'scr/data/products_{city}.json',
                #     'w',
                #     encoding='utf-8'
                # ) as file:
                #     json.dump(products, file, indent=4, ensure_ascii=False)
    except Exception as error:
        logger.critical(msg=error, exc_info=True)
        sys.exit()


if __name__ == '__main__':
    main()
