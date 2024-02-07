import asyncio
from celery import shared_task

from parsing_stores.lenta.main import main_ as main_lenta


@shared_task
def run_src_lenta():
    asyncio.run(main_lenta())


@shared_task
def run_src_magnit():
    pass
