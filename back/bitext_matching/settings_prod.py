from .settings import *
from .env_settings import *

DEBUG = False

STATIC_ROOT = '/code/static/'

ALLOWED_HOSTS = [
    'delorean.fdesousa.fr'
]

INSTALLED_APPS.append('mod_wsgi.server')

CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = [
    'http://alignment.fdesousa.fr'  # Allow only the React frontend to send graphQL queries
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': DATABASE_NAME,                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': DATABASE_USER,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': 'localhost',             # Empty for localhost through domain sockets or           '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}
