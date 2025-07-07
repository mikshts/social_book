# File: social_book/social_book/settings.py

from pathlib import Path
import os
import dj_database_url
# import cloudinary # Already imported by cloudinary_storage, but no harm in explicit import
# import cloudinary_storage # Already imported implicitly by DEFAULT_FILE_STORAGE, no harm in explicit import

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-default-key")
DEBUG = os.environ.get("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# APPLICATIONS
INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'core.apps.CoreConfig', # Your app
    'cloudinary', # Keep this here
    'cloudinary_storage', # Keep this here, but remember the order rule
]

# CRITICAL CHANGE 1: Correct INSTALLED_APPS order for Cloudinary
# 'cloudinary_storage' MUST come BEFORE 'django.contrib.staticfiles'
# 'cloudinary' can be anywhere, but typically near cloudinary_storage
INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage', # MOVED UP
    'django.contrib.staticfiles', # MOVED DOWN
    'channels',
    'core.apps.CoreConfig',
    'cloudinary', # Good position
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.UpdateLastActivityMiddleware',
]

ROOT_URLCONF = 'social_book.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI/ASGI
WSGI_APPLICATION = 'social_book.wsgi.application'
ASGI_APPLICATION = 'social_book.asgi.application'

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL)
    }
else:
    # Local fallback to SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }


# CRITICAL CHANGE 2: Cloudinary authentication
# You are using CLOUDINARY_URL, which is fine, but it combines all credentials.
# However, if you explicitly set CLOUDINARY_CLOUD_NAME, API_KEY, API_SECRET,
# those will override the CLOUDINARY_URL for individual components.
# It's usually best to stick to one method. If you use CLOUDINARY_URL, make sure it's correct.
# If you prefer separate variables, then use those.

# Let's assume you're using CLOUDINARY_URL for simplicity as you have it.
# The important part is that this environment variable MUST BE CORRECTLY SET ON RENDER.
CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL') # This loads the full URL from Render env var

# If you prefer separate variables (which gives more control and can be easier to debug):
# import cloudinary # Make sure this is imported at the top
# cloudinary.config(
#     cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
#     api_key=os.environ.get('CLOUDINARY_API_KEY'),
#     api_secret=os.environ.get('CLOUDINARY_API_SECRET')
# )

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage' # GOOD, this is correct.

# CHANNELS (Redis) na pulihan ini diri haaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa--------
import os

REDIS_URL = os.environ.get("REDIS_URL", "redis://127.0.0.1:6379")

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
        },
    },
}



# These print statements are helpful for debugging on Render logs
print("DEBUG:", DEBUG) # Add this to see if DEBUG is True/False
print("ALLOWED_HOSTS:", ALLOWED_HOSTS) # Add this
print("Redis URL:", REDIS_URL) # Keep this
print("Cloudinary URL:", CLOUDINARY_URL) # Keep this

# PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# TIME/LOCALE
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Manila'
USE_I18N = True
USE_TZ = True

# STATIC
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# MEDIA - GOOD. You don't explicitly need MEDIA_URL/ROOT to serve from Cloudinary,
# but Django still uses them internally, e.g., for admin uploads before default storage takes over.
# It's fine to leave them implied or uncomment them if you had them before.
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media' # This is good practice to define where media *would* go locally.

# DEFAULT FIELD
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# SECURITY FOR PRODUCTION
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CSRF_TRUSTED_ORIGINS = os.environ.get(
    "CSRF_TRUSTED_ORIGINS",
    "https://perfectmatch-0uig.onrender.com" # Ensure this is your actual Render URL
).split(",")