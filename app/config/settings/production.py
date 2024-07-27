# import here the file from base.py
# for example: from .base import *
# from celery.schedules import crontab
# from decouple import config

# Media and static files
# Add settings for media files like images and videos (AWS S3, Cloudinary, etc.)

# Celery

# CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://redis:6379/0')
# CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='redis://redis:6379/0')
#
# CELERY_BEAT_SCHEDULE = {
#     'example_task': {
#         'task': 'app.tasks.example_task',
#         # Activate example_task every month on the 1st day at 2:00 AM
#         'schedule': crontab(minute='0', hour='2', day_of_month='1'),
#     },
# }

