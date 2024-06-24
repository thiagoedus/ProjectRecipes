from .environment import BASE_DIR

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'base_static',
]
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


INTERNAL_IPS = [
    "127.0.0.1",
]