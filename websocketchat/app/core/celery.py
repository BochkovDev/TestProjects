import os

from celery import Celery

from .settings import settings


app = Celery('core', broker=settings.CELERY.BROKER_URL)

app.conf.update(
    result_backend=settings.CELERY.RESULT_BACKEND,
    task_track_started=settings.CELERY.TASK_TRACK_STARTED,
    task_time_limit=settings.CELERY.TASK_TIME_LIMIT,
    timezone=settings.CELERY.TIMEZONE,
    accept_content=settings.CELERY.ACCEPT_CONTENT.split(','),
    result_serializer=settings.CELERY.RESULT_SERIALIZER,
    task_serializer=settings.CELERY.TASK_SERIALIZER,
    broker_connection_retry_on_startup=settings.CELERY.BROKER_CONNECTION_RETRY_ON_STARTUP,
)

app.autodiscover_tasks(['services'])