import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.getenv("SECRET_KEY"))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "apps.core",
    "apps.catalog",
    "apps.profile",
    "frontend",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "diploma.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "diploma.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTH_USER_MODEL = "auth.User"

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Directories to search for static files

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    # "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
}

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000', "http://localhost"
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "main": {
            "format": "%(levelname)-8s %(asctime)s %(name)s:%(lineno)d  >  %(message)s",
            "style": "%",
        },
    },
    "handlers": {
        "file_django": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs/service_django.log",
            "formatter": "main",
        },
        "file_site": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs/service.log",
            "formatter": "main",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file_django"],
            "level": "WARNING",
            "propagate": True,
        },
        "django.request": {
            "handlers": ["file_django"],
            "level": "DEBUG",
            "propagate": False,
        },
        "apps": {
            "handlers": ["file_site"],
            "level": "DEBUG",
        },
    },
}
