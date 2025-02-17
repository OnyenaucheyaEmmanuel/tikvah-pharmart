from .devlopement import *
import os
from dotenv import load_dotenv
load_dotenv()

import os

BASE_DIR = Path(__file__).resolve().parent.parent

WSGI_APPLICATION = 'onlineretailpos.wsgi.application'
DEBUG = True
SECRET_KEY = 'i5bp(^x7@ys9yi^phvxy7n&4uin#mrcb$y62dmok8#m*hbkj2u'

ALLOWED_HOSTS = ['127.0.0.1', 'localhost','tikvahpharmacy.onrender.com']

# SITE_ID = 7


# CSRF_TRUSTED_ORIGINS = ['https://*.127.0.0.1']


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}



# HTTPS Security - Django
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

# HSTS Security - Django
SECURE_HSTS_SECONDS = 120
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


