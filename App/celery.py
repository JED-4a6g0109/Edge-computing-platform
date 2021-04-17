import os

from celery import Celery
from celery.schedules import crontab
from celery.schedules import timedelta
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'App.settings')

app = Celery('App',backend='redis://localhost:6379/1', broker='redis://localhost:6379/0')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
CELERY_RESULT_BACKEND = 'django-db'


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


