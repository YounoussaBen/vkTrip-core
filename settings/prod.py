from .dev import *
import os
from dotenv import load_dotenv
import dj_database_url

# Load environment variables
load_dotenv()

# Override the DEBUG setting to False for production
DEBUG = os.getenv('DEBUG', '0').lower() in ['true', 't', '1']

# Update the database settings for production, using the DATABASE_URL environment variable
DATABASES = {
    'default': dj_database_url.parse(os.getenv('DATABASE_URL'), conn_max_age=600),
}

# Retrieve ALLOWED_HOSTS from the environment variable

# Split the allowed_hosts_env by comma to create a list of allowed hosts
ALLOWED_HOSTS = [os.getenv('ALLOWED_HOSTS_RENDER')]

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Override static files storage setting for production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

