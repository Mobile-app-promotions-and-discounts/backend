from __future__ import absolute_import, unicode_literals
from celery import shared_task

from parsing_stores.lenta.scr.add_to_db import add_store_products_in_db


@shared_task
def run_src_lenta():
    print('ТАСКА ТАСКА ТАСКА ТАСКА')


@shared_task
def add_store_products_in_db_task(products_in_store, store_data):
    add_store_products_in_db(products_in_store, store_data)
