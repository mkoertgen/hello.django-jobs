from logging.config import dictConfig
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('FLASK_DEBUG', '') != '0'

# Database
DATA_DIR = os.environ.get('DATA_DIR', BASE_DIR)

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(DATA_DIR, 'db.sqlite3')}"

#### Logging ##############################################################
# Docker, 12x factor app:
# - log to stdout / stderr
# - log in json format
# cf.: https://lincolnloop.com/blog/django-logging-right-way/
LOGLEVEL = os.environ.get('LOGLEVEL', 'DEBUG' if DEBUG else 'INFO').upper()


def formatter():
    json_format = os.environ.get('LOG_JSON', str(not DEBUG)) == 'True'
    if json_format:
        return {'class': 'logstash_formatter.LogstashFormatterV1'}
    return {'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'}


# logging dictConfig configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {'console': formatter()},
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': LOGLEVEL
        },
    },
}

dictConfig(LOGGING)
