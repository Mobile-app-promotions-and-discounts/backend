import asyncio
import logging
import sys
from datetime import datetime
from logging.config import fileConfig
from typing import List

import parsing_stores.lenta.scr.config as cfg
# from parsing_stores.tasks import add_store_products_in_db_task
# from parsing_stores.lenta.scr.add_to_db import add_store_products_in_db
from parsing_stores.lenta.scr.core import open_json_file
from parsing_stores.lenta.scr.scr_products import aget_products_in_store
from parsing_stores.lenta.scr.scr_stores import (get_and_save_all_stores,
                                                 get_and_save_stores_in_city)

fileConfig('logging.ini')
logger = logging.getLogger()

PARSING_OK = 'Все данные по городу {} добавлены в БД {}. Время парсинга составило {}'


async def main_() -> None:
    start_parsing = datetime.today()
    try:
        get_and_save_all_stores()
        for city in cfg.CITY_APPLICATIONS:
            get_and_save_stores_in_city(city)
            stores_in_city: List[dict] = open_json_file(cfg.FILE_NAME['STORES_IN_SITY'].format(city))[:10]
            results_scr = await asyncio.gather(
                *[asyncio.create_task(aget_products_in_store(store)) for store in stores_in_city]
            )
            # for products_in_store in results_scr:
            #     add_store_products_in_db_task.delay(*products_in_store)
            logger.debug(
                msg=PARSING_OK.format(
                    city,
                    datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
                    datetime.today() - start_parsing
                )
            )
    except Exception as error:
        logger.critical(msg=error, exc_info=True)
        sys.exit()


if __name__ == '__main__':
    asyncio.run(main_())
