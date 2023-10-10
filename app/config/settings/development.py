from .base import os, BASE_DIR

# Media and static files
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '../../core/', 'mediafiles')

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, '../../core/', 'staticfiles')
