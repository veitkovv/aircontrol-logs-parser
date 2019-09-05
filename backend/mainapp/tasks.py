from backend.celery import app
from .utils import scan_logs, start_roll_fabric
from django.conf import settings


@app.task
def scan_logs_task():
    my_result = scan_logs(settings.LOGS_PATH)  # Скан файловой системы
    start_roll_fabric(my_result)
