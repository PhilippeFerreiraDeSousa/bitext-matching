from .settings import *
from .env_settings import SECRET_KEY

DEBUG = False

STATIC_ROOT = '/code/static/'

ALLOWED_HOSTS = [
    'delorean.fdesousa.fr'
]

DATABASES['default']['OPTIONS']['read_default_file'] = os.path.join(BASE_DIR, 'db.cnf'),

INSTALLED_APPS.append('mod_wsgi.server')

CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = [
    'http://alignment.fdesousa.fr'  # Allow only the React frontend to send graphQL queries
]
