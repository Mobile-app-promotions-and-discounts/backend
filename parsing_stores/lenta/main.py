import logging
import sys
from datetime import datetime
from logging.config import fileConfig

import scr.config as cfg
import scr.msg as msg
from scr.core import open_json_file
from scr.add_to_db import add_to_db
from scr.scr_products import get_products_in_store
from scr.scr_stores import (get_and_save_all_stores,
                            get_and_save_stores_in_city)


fileConfig('logging.ini')
logger = logging.getLogger()


def main():
    try:
        get_and_save_all_stores()
        for city in cfg.CITY_APPLICATIONS:
            get_and_save_stores_in_city(city)
            stores_in_city = open_json_file(cfg.FILE_NAME['STORES_IN_SITY'].format(city))
            for store in stores_in_city:
                add_to_db(*get_products_in_store(store))
            logger.debug(
                msg=msg.PARSING_OK.format(city, datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            )
    except Exception as error:
        logger.critical(msg=error, exc_info=True)
        sys.exit()


if __name__ == '__main__':
    main()
