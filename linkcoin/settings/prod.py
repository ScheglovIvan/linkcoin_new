from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#fb2oau@2kw^wpojje&+yg9_ro=(rci)%s__k9k4m1*mvms@h!4t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': f'{DIRNAME}/linkcoin/settings/db_configs/prod.cnf'
        }
    }
}

AUTH_USER_MODEL = 'register.User'

# Email
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'linkcoin@thelinkcoin.com'
EMAIL_HOST_PASSWORD = 'Patrearh6'
EMAIL_PORT = 465

# PayPal
PAYPAL_CLIENT_ID = "AbiyMPGlIRoOsUDQDQ9tIPtvmQpDJJH7VdnHSDcW7lQM9-0F8NvBGNAHKWOgHk27B4TsZWcA5n0UtN3-"
PAYPAL_SECRET_KEY = "EObBYUP5wf5b5J8AE6D1MF4XzIRSfKVSP7sMLXhDBp5yAAeCBD3Q-mIh94slNHGyaEhtzqUEMoqYwjZ0"
PAYPAL_MODE = "sandbox" # sandbox or live


# Coinbase
COMMERCE_COINBASE_API_KEY = "a1e4cbe8-628a-4b99-9f3c-365e837af595"
COINBASE_API_KEY = "xVTwCaD9jFlx9Qa3"
COINBASE_SECRET_KEY = "IyF4KVqezAlHLGyrbdzdILhrVIWo71jM"
