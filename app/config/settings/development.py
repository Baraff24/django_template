from celery.schedules import crontab
from decouple import config
from .base import *

# Media and static files
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '../../core/', 'mediafiles')

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, '../../core/', 'staticfiles')


# Celery

CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://redis:6379/0')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='redis://redis:6379/0')

CELERY_BEAT_SCHEDULE = {
    'renew-ssl-certificate': {
        'task': 'app.tasks.renew_ssl_certificate',
        # Renew SSL certificate every month on the 1st day at 2:00 AM
        'schedule': crontab(minute='0', hour='2', day_of_month='1'),
    },
}
