import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'scan-cinegy-logs-every-morning': {
        'task': 'mainapp.tasks.scan_logs_task',
        'schedule': crontab(hour=6, minute=15),  # Daily @ 6:15 am
    },
}
app.conf.timezone = settings.TIME_ZONE
