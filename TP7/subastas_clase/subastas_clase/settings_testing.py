from settings import *

SECRET_KEY = 'django-insecure-ogj^q#mk!a9y20w9yh$&ch2xz($n_aprls6-czdvus0hgfbri2'

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}




