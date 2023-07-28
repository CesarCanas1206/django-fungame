import os
import environ
from pathlib import Path
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


env = environ.Env()
env.read_env(str(BASE_DIR / ".env"))


# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "UTC"
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en-us"
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths


# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default="postgres:///core",
    ),
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
# https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-DEFAULT_AUTO_FIELD
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.humanize",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
]
THIRD_PARTY_APPS = [
    "widget_tweaks",
    "currencies",
    "ckeditor",
    "ckeditor_uploader",
    "django_filters",
    "fullurl",
    "crispy_forms",
    "crispy_bootstrap5",
    "captcha",
    "django_htmx",
    "easy_thumbnails",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
]

LOCAL_APPS = [
    "accounts",
    "coinbase",
    "payment",
    "main",
    "blog",
    "wowtbc",
    "shop",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "main.middleware.MainMiddleware",
]

ROOT_URLCONF = "fungame.urls"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"


WSGI_APPLICATION = "fungame.wsgi.application"


# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(BASE_DIR / "staticfiles")
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [str(BASE_DIR / "static")]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(BASE_DIR / "media")
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#dirs
        "DIRS": [str(BASE_DIR / "templates")],
        # https://docs.djangoproject.com/en/dev/ref/settings/#app-dirs
        "APP_DIRS": True,
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                # `allauth` needs this from django
                "django.template.context_processors.request",
            ],
        },
    }
]


AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# ck editor settings
CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_CONFIGS = {
    "default": {
        "contentsCss": "https://virtgold.s3.amazonaws.com/static/assets/css/bootstrap.min.css",
        "CKEDITOR_IMAGE_MAX_WIDTH": "100%",
        "fullPage": "true",
        "height": 600,
        "width": "150%",
        "toolbar": "Custom",
        "toolbar_Custom": [
            [
                "Format",
                "Bold",
                "Italic",
                "Underline",
                "Strike",
                "NumberedList",
                "BulletedList",
            ],
            ["Link", "Unlink", "Anchor"],
            ["Image", "Table", "HorizontalRule", "SpecialChar"],
            ["Source"],
        ],
    },
}

# credentials
RECAPTCHA_PUBLIC_KEY = env.str("RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = env.str("RECAPTCHA_PRIVATE_KEY")
OPENEXCHANGERATES_APP_ID = env.str("OPENEXCHANGERATES_APP_ID")
STRIPE_SECRET_KEY = env.str("STRIPE_SECRET_KEY")
STRIPE_PUBLIC_KEY = env.str("STRIPE_PUBLIC_KEY")

COINBASE_API_KEY = env.str("COINBASE_API_KEY")
COINBASE_SECRET_KEY = env.str("COINBASE_SECRET_KEY")


THUMBNAIL_ALIASES = {
    "": {
        "icon": {
            "size": (30, 30),
            "detail": False,
            "crop": True,
            "upscale": False,
            "ALIAS": "icon",
            "ratio_field": "crop_thumb",
        },
        "small": {
            "size": (160, 75),
            "detail": False,
            "crop": True,
            "upscale": False,
            "ALIAS": "small",
            "ratio_field": "crop_thumb",
        },
        "medium": {
            "size": (342, 191),
            "detail": False,
            "crop": True,
            "upscale": False,
            "ALIAS": "medium",
            "ratio_field": "crop_thumb",
        },
        "large": {
            "size": (350, 120),
            "quality": 90,
            "detail": True,
            "upscale": False,
            "ALIAS": "large",
            "ratio_field": "crop_image",
        },
    },
}

# Django Allauth
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# import reverse

LOGIN_REDIRECT_URL = reverse_lazy("account_profile")
