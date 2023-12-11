import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kakao_py39.settings')

app = Celery('kakao_py39')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
