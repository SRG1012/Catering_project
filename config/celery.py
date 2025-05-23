import os
 
from celery import Celery
 
 # Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
 
celery_app = Celery("config")

celery_app.config_from_object("django.conf:settings", namespace="CELERY")
#app.conf.update(task_serializer="pickle")
 
 # Load task modules from all registered Django apps.
celery_app.autodiscover_tasks()