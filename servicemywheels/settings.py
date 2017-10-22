"""
Django settings for serviceMyWheels project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
from .email_info import *

# for gmail or google apps
# EMAIL_BACKEND =EMAIL_BACKEND
# EMAIL_USE_TLS = EMAIL_USE_TLS
# EMAIL_HOST = EMAIL_HOST
# EMAIL_HOST_USER = EMAIL_HOST_USER
# EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
# EMAIL_PORT = EMAIL_PORT
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = EMAIL_USE_TLS
EMAIL_HOST = EMAIL_HOST
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
EMAIL_PORT = EMAIL_PORT
SERVER_EMAIL = SERVER_EMAIL

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(__file__)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-d0gr6nch*n7$@)5id=81=b^o$&kpn37=lx8((s1m%i=ixcx35'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #Local Apps
    'website',
    'core',
	'notifications',

    #TPT Apps
    'rest_framework',
    'bootstrapform',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    'django.core.context_processors.request',
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "core.context_processors.make_session_available",
    # "servicemywheels.context_processors.baseurl",
    # "servicemywheels.context_processors.baseurlwithoutslash",
    "servicemywheels.context_processors.s3url",
    # "servicemywheels.context_processors.ftpurl"
)

ROOT_URLCONF = 'servicemywheels.urls'

WSGI_APPLICATION = 'servicemywheels.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'serviceMyWheels',
        'USER': 'root',
        'PASSWORD': 'asdf123',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

# STATIC_URL = '/static/'

STATICFILES_DIRS = (
os.path.join(BASE_DIR, 'static'),
)

STATIC_URL = '/static/'
TEMPLATE_DIRS = (
    BASE_DIR + '/templates/',
)

AUTH_USER_MODEL = 'core.Customers'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}



FACEBOOK_APP_ID = '1486735948287462'  # ServiceMyWheels app with a/c: dinesh.mca.iitr@gmail.com
FACEBOOK_APP_SECRET = '42c351e48699aa5451a2c505288799ab'

GOOGLE_PLUS_APP_ID = '111013748921-6tmu37tlf6uga60tgeq0qero83kif0aj.apps.googleusercontent.com'
GOOGLE_PLUS_APP_SECRET = 'hX4FxiszLdIxA-KyfDRY-s5Z'

REST_FRAMEWORK = {
'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),
}


SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 60 * 60

