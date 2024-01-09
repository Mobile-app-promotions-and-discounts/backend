from celery import shared_task

from parsing_stores.magnit.get_stores import main


@shared_task
def parse_stores_magnit():
    main()
