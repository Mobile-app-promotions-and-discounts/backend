from __future__ import absolute_import, unicode_literals
from celery import shared_task


@shared_task
def run_src_lenta():
    print('ТАСКА ТАСКА ТАСКА ТАСКА')
