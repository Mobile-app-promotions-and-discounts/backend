import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cherry.settings')

app = Celery('cherry')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# Запуск каждый день в 00:00
app.conf.beat_schedule = {
    'auto_run_src_lenta': {
        'task': 'parsing_stores.tasks.run_src_lenta',
        'schedule': crontab(minute=0, hour=0)
    },
    'auto_run_src_magnit': {
        'task': 'parsing_stores.tasks.run_src_magnit',
        'schedule': crontab(minute=0, hour=0)
    },
}
