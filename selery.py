import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cherry.settings')

app = Celery('cherry')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'run_parsing': {
        'task': 'parsing_stores.tasks.run_src_lenta',
        'schedule': crontab(minute='*/1')
    },
}


@app.task()
def debag_task():
    print('debag_task debag_task debag_task')