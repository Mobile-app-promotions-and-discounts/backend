import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cherry.settings')

app = Celery('cherry')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_notifications': {
        'task': 'parsing_stores.tasks.run_src_lenta',
        'schedule': crontab()
    },
}


@app.task(bind=True)
def debug_task(self):
    print('ЗАПУСК debug_task')
