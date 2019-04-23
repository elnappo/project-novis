"""
For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import socket

import dj_database_url
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from setuptools_scm import get_version


def bool_env(key, default=None):
    true_values = ('yes', 'y', 'true', '1')
    false_values = ('no', 'n', 'false', '0', '')
    value = os.environ.get(key)

    if default not in (True, False):
        raise ValueError(
            'Default value {0!r} is not a boolean value'.format(default))

    if value is None:
        return default

    normalized_value = value.strip().lower()

    if normalized_value in true_values:
        return True
    elif normalized_value in false_values:
        return False
    else:
        raise ValueError('Cannot interpret boolean value {0!r}'.format(key))


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define if run in production mode
PRODUCTION = bool_env("DJANGO_PRODUCTION", False)

# SECURITY WARNING: don't run with debug turned on in production!
if PRODUCTION:
    # Ensure production does not run with DEBUG on
    DEBUG = False
else:
    DEBUG = bool_env("DJANGO_DEBUG", True)

if not DEBUG:
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    USE_X_FORWARDED_HOST = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    CSP_UPGRADE_INSECURE_REQUESTS = True
    CSP_BLOCK_ALL_MIXED_CONTENT = True
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"

else:
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "INSECURE")

ALLOWED_HOSTS = [os.environ.get("DJANGO_ALLOWED_HOSTS", "*")]


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'django.contrib.sitemaps',
    'django.contrib.gis',

    'project_novis.accounts.apps.AccountsConfig',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_gis',
    'django_filters',
    'drf_yasg',
    'oauth2_provider',
    'crispy_forms',
    'avatar',

    'project_novis.callsign.apps.CallsignConfig',
    'project_novis.main.apps.MainConfig',
    'project_novis.radius.apps.RadiusConfig',
]

MIDDLEWARE = [
    'project_novis.main.middleware.HealthCheckMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django_referrer_policy.middleware.ReferrerPolicyMiddleware',
    'csp.middleware.CSPMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

# Django Debug Toolbar
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ['127.0.0.1']

ROOT_URLCONF = 'project_novis.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG,
        },
    },
]

DATABASES = {
    'default': dj_database_url.config(default=os.environ.get("DATABASE_URL", "postgis://postgres:postgres@127.0.0.1:5432/postgres"))
}

# DATABASES["default"]["OPTIONS"]["connect_timeout"] = 5

WSGI_APPLICATION = 'project_novis.wsgi.application'

SITE_ID = 1

VERSION = get_version(root='../', relative_to=__file__)

HOSTNAME = socket.gethostname()

# Security settings
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
REFERRER_POLICY = 'strict-origin-when-cross-origin'

# Content-Security-Policy - https://django-csp.readthedocs.io/en/latest/configuration.html
CSP_REPORT_ONLY = True
CSP_DEFAULT_SRC = ("'none'", )
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "cdnjs.cloudflare.com", "maxcdn.bootstrapcdn.com", "piwik.nerdpol.io", "stackpath.bootstrapcdn.com")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "maxcdn.bootstrapcdn.com", "cdnjs.cloudflare.com", "fonts.googleapis.com", "stackpath.bootstrapcdn.com")
CSP_FONT_SRC = ("'self'", "fonts.googleapis.com", "fonts.gstatic.com", "maxcdn.bootstrapcdn.com", "cdnjs.cloudflare.com", "stackpath.bootstrapcdn.com")
CSP_IMG_SRC = ("'self'", "data:", "cdnjs.cloudflare.com", "piwik.nerdpol.io", "www.gravatar.com")
CSP_EXCLUDE_URL_PREFIXES = ("/admin/", "/api/v1/swagger/")

# CORS settings
CORS_URLS_REGEX = r'^/api/.*$'
# For OAuth2
# CORS_URLS_REGEX = r'^(/api/|/o/).*$'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'accounts.User'
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = "mandatory"

LOGIN_REDIRECT_URL = "/"

OAUTH2_PROVIDER = {
    'SCOPES': {'user:write': 'Grants read/write access to user data',
               'user:read': 'Grants access to read user data'}
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    )
}

CRISPY_TEMPLATE_PACK = 'bootstrap3'

DJANGO_SENTRY_DSN = os.environ.get("DJANGO_SENTRY_DSN", None)

# Sentry settings
if not DEBUG and DJANGO_SENTRY_DSN:
    sentry_sdk.init(
        dsn=DJANGO_SENTRY_DSN,
        integrations=[DjangoIntegration(), ],
        release=VERSION,
        environment=os.environ.get("DJANGO_SENTRY_ENVIRONMENT", "unknown")
    )

    # https://docs.sentry.io/error-reporting/security-policy-reporting/
    CSP_REPORT_URI = (f"https://sentry.io/api/{ DJANGO_SENTRY_DSN.split('/')[3] }/security/?sentry_key={ DJANGO_SENTRY_DSN.split('/')[2].split('@')[0] }",)

# Email settings
if not DEBUG and os.environ.get("DJANGO_EMAIL_HOST_PASSWORD", False):
    DEFAULT_FROM_EMAIL = os.environ.get("DJANGO_DEFAULT_FROM_EMAIL", "info@project-novis.org")
    SERVER_EMAIL = os.environ.get("DJANGO_SERVER_EMAIL", "root@project-novis.org")

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.environ.get("DJANGO_EMAIL_HOST", "mail.gandi.net")
    EMAIL_HOST_USER = os.environ.get("DJANGO_EMAIL_HOST_USER", "info@project-novis.org")
    EMAIL_HOST_PASSWORD = os.environ.get("DJANGO_EMAIL_HOST_PASSWORD")
    EMAIL_PORT = os.environ.get("DJANGO_EMAIL_PORT", "587")
    EMAIL_USE_TLS = True
    EMAIL_SUBJECT_PREFIX = os.environ.get("DJANGO_EMAIL_SUBJECT_PREFIX", "")
    # EMAIL_TIMEOUT = 60
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
WHITENOISE_ROOT = os.path.join(os.path.join(BASE_DIR, "static"), "web_root")

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

DOCS_URL = "https://project-novis.readthedocs.io/en/latest/"
