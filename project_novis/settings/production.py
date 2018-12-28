import socket

from setuptools_scm import get_version

from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = ["www.project-novis.org"]

CORS_ORIGIN_ALLOW_ALL = False
#CORS_ORIGIN_WHITELIST = ("",)

DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': 'postgres',
            'USER': 'postgres',
            'PASSWORD': '',
        }
}


SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEFAULT_FROM_EMAIL = "info@project-novis.org"
SERVER_EMAIL = "root@project-novis.org"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "mail.gandi.net"
EMAIL_HOST_USER = "info@project-novis.org"
EMAIL_HOST_PASSWORD = ""
EMAIL_PORT = "587"
EMAIL_USE_TLS = True
EMAIL_SUBJECT_PREFIX = ""
#EMAIL_TIMEOUT = 60
