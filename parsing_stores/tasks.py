import asyncio
from celery import shared_task
# from django.db.utils import DatabaseError

# from parsing_stores.lenta.scr.add_to_db import add_store_products_in_db
from parsing_stores.lenta.main import main_ as main_lenta


@shared_task
def run_src_lenta():
    asyncio.run(main_lenta())


# @shared_task
# def run_src_magnit():
#     pass


# @shared_task
# def add_store_products_in_db_task(products_in_store, store_data):
#     add_store_products_in_db(products_in_store, store_data)
