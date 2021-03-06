# -*- coding: utf-8 -*-
import sys
import logging

import os
import environ

ROOT_DIR = environ.Path(__file__) - 2
APPS_DIR = ROOT_DIR.path('steelkiwi_python_test_task')
sys.path.append('steelkiwi_python_test_task/apps')

env = environ.Env(
    DJANGO_DEBUG=(bool, False),
    DJANGO_SECRET_KEY=(str, ''),
    DJANGO_ADMINS=(list, []),
    DJANGO_ALLOWED_HOSTS=(list, []),
    # Static/Media
    DJANGO_STATIC_ROOT=(str, str(APPS_DIR('staticfiles'))),
    DJANGO_MEDIA_ROOT=(str, str(APPS_DIR('media'))),
    # Database
    POSTGRES_HOST=(str, 'db'),
    POSTGRES_PORT=(int, 5432),
    POSTGRES_DB=(str, ''),
    POSTGRES_USER=(str, ''),
    POSTGRES_PASSWORD=(str, ''),
    # Email
    DJANGO_EMAIL_URL=(environ.Env.email_url_config, 'consolemail://'),
    DJANGO_EMAIL_BACKEND=(str, 'django.core.mail.backends.smtp.EmailBackend'),
    DJANGO_DEFAULT_FROM_EMAIL=(str, 'admin@example.com'),
    DJANGO_SERVER_EMAIL=(str, 'root@localhost.com'),
    # FOR CELERY
    BROKER_URL=(str, 'redis://localhost:6379'),
    CELERY_RESULT_BACKEND=(str, 'redis://localhost:6379'),
    CELERY_ACCEPT_CONTENT=(list, ['application/json']),
    CELERY_TASK_SERIALIZER=(str, 'json'),
    CELERY_RESULT_SERIALIZER=(str, 'json'),
)
environ.Env.read_env(env_file=os.path.join(str(ROOT_DIR), '.env'))

DEBUG = env.bool("DJANGO_DEBUG")
SECRET_KEY = env('DJANGO_SECRET_KEY')
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')
ADMINS = tuple([
    tuple(admins.split(':'))
    for admins in env.list('DJANGO_ADMINS')
])
MANAGERS = ADMINS
ADMIN_URL = 'admin/'
ADMIN_SITE_TITLE = 'Steelkiwi Python Test Task'
ADMIN_SITE_HEADER = 'Steelkiwi Python Test Task'
TIME_ZONE = 'UTC'
USE_TZ = True
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True

SITE_ID = 1

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST'),
        'PORT': env('POSTGRES_PORT'),
    }
}

DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
)

THIRD_PARTY_APPS = (
    'django_extensions',
    'rest_framework',
    'django_filters',
    'drf_yasg',
)

LOCAL_APPS = (
    'redirects_analyzer.apps.RedirectsAnalyzerAppConfig',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

EMAIL_URL = env.email_url('DJANGO_EMAIL_URL')
EMAIL_BACKEND = EMAIL_URL['EMAIL_BACKEND']
EMAIL_HOST = EMAIL_URL.get('EMAIL_HOST', '')
EMAIL_HOST_PASSWORD = EMAIL_URL.get('EMAIL_HOST_PASSWORD', '')
EMAIL_HOST_USER = EMAIL_URL.get('EMAIL_HOST_USER', '')
EMAIL_PORT = EMAIL_URL.get('EMAIL_PORT', '')
EMAIL_USE_SSL = 'EMAIL_USE_SSL' in EMAIL_URL
EMAIL_USE_TLS = 'EMAIL_USE_TLS' in EMAIL_URL
EMAIL_FILE_PATH = EMAIL_URL.get('EMAIL_FILE_PATH', '')
EMAIL_SUBJECT_PREFIX = ''
DEFAULT_FROM_EMAIL = env('DJANGO_DEFAULT_FROM_EMAIL')
SERVER_EMAIL = env('DJANGO_SERVER_EMAIL')

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [
        str(APPS_DIR.path('templates')),
    ],
    'OPTIONS': {
        'debug': DEBUG,
        'loaders': [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ],
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.template.context_processors.i18n',
            'django.template.context_processors.media',
            'django.template.context_processors.static',
            'django.template.context_processors.tz',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'INFO',
            'propagate': True
        },
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = env('DJANGO_STATIC_ROOT')
STATICFILES_DIRS = (
    str(APPS_DIR.path('static')),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

MEDIA_URL = '/media/'
MEDIA_ROOT = env('DJANGO_MEDIA_ROOT')

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

# FOR CELERY
BROKER_URL = env('BROKER_URL')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND')
CELERY_ACCEPT_CONTENT = env('CELERY_ACCEPT_CONTENT')
CELERY_TASK_SERIALIZER = env('CELERY_TASK_SERIALIZER')
CELERY_RESULT_SERIALIZER = env('CELERY_RESULT_SERIALIZER')
