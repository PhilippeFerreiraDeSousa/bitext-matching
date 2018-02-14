from .settings import *
from .env_settings import SECRET_KEY

DEBUG = False

STATIC_ROOT = '/code/static/'

ALLOWED_HOSTS = [
    'delorean.fdesousa.fr'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(BASE_DIR, 'db.cnf'),
            'init_command': 'SET default_storage_engine=INNODB'
        },
    }
}

INSTALLED_APPS.append('mod_wsgi.server')

CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = [
    'alignment.fdesousa.fr'  # Allow only the React frontend to send graphQL queries
]
