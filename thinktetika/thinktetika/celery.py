import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thinktetika.settings')
celery_app = Celery('thinktetika')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()

celery_app.conf.beat_schedule = {
    'send-report-every-single-minute': {
        'task': 'main.tasks.sending_new_products_by_scheduler',
        'schedule': crontab(minute=59, hour=17, day_of_week=1),
    },
}
