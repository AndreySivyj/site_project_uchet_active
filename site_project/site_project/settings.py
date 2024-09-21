"""
Django settings for site_project project.

Generated by 'django-admin startproject' using Django 4.2.14.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

from decouple import config
import os

import ldap
from django_auth_ldap.config import LDAPSearch, LDAPGroupQuery, GroupOfNamesType, PosixGroupType, LDAPSearchUnion
from django.contrib.messages import constants as messages
import logging

logger = logging.getLogger('django_auth_ldap')
logger.addHandler(logging.StreamHandler())
# logger.setLevel(logging.WARNING)
logger.setLevel(logging.DEBUG)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", cast=bool)

ALLOWED_HOSTS = [config("HOST_IP"), '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'crispy_forms',
    'crispy_bootstrap5',
    'widget_tweaks',
    'django_select2',
    # 'ajax_select',

    'debug_toolbar',
    'auth_users.apps.AuthUsersConfig',        
    'uchet_active.apps.UchetActiveConfig',

]


CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'site_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'site_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config("DATABASES_NAME"),
        'USER': config("DATABASES_USER"),
        'PASSWORD': config("DATABASES_PASSWORD"),
        'HOST': 'localhost',
        'PORT': config("DATABASES_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ru-ru'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

# USE_TZ = True
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'





STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

LOGIN_URL = '/auth_users/login/'
LOGIN_REDIRECT_URL = '/'

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-successs',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}


LDAP_IGNORE_CERT_ERRORS = True
AUTH_LDAP_START_TLS = False
AUTH_LDAP_SERVER_URI = config("AUTH_LDAP_SERVER_URI")
AUTH_LDAP_AUTHORIZE_ALL_USERS = True
AUTH_LDAP_PERMIT_EMPTY_PASSWORD = True
AUTH_LDAP_BIND_DN = config("AUTH_LDAP_BIND_DN")
AUTH_LDAP_BIND_PASSWORD = config("AUTH_LDAP_BIND_PASSWORD")

AUTH_LDAP_USER_SEARCH = LDAPSearchUnion(
    LDAPSearch(config("AUTH_LDAP_USER_SEARCH_LDAPSearch1"),ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)"),
    LDAPSearch(config("AUTH_LDAP_USER_SEARCH_LDAPSearch2"),ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)"),
    LDAPSearch(config("AUTH_LDAP_USER_SEARCH_LDAPSearch3"),ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)"),
    LDAPSearch(config("AUTH_LDAP_USER_SEARCH_LDAPSearch4"),ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)"),
)

AUTH_LDAP_GROUP_SEARCH = LDAPSearch(config("AUTH_LDAP_GROUP_SEARCH_LDAPSearch"),ldap.SCOPE_SUBTREE, "(objectClass=Group)")
AUTH_LDAP_GROUP_TYPE = GroupOfNamesType(name_attr="cn")

## AUTH_LDAP_GROUP_TYPE = PosixGroupType(name_attr="cn")

AUTH_LDAP_REQUIRE_GROUP = (
    LDAPGroupQuery(config("AUTH_LDAP_REQUIRE_GROUP_LDAPGroupQuery1"))|
    LDAPGroupQuery(config("AUTH_LDAP_REQUIRE_GROUP_LDAPGroupQuery2"))|
    LDAPGroupQuery(config("AUTH_LDAP_REQUIRE_GROUP_LDAPGroupQuery3"))#|
)

AUTH_LDAP_USER_ATTR_MAP = {
        "username": "sAMAccountName",
        "first_name": "givenName",
        "last_name": "sn",
        "email": "mail",
        
        # "password": "userPassword",
}

# для нескольких групп используем формат списка - "is_staff": ["cn=WG_Access_Print", "cn=WG_Admin_Print"],
AUTH_LDAP_USER_FLAGS_BY_GROUP = { 
        "is_active": [
                        config("AD_object_Active"),
                        config("AD_object_Staf"),
                        config("AD_object_Admin")],
        
        "is_staff": [
                        config("AD_object_Staf"),
                        config("AD_object_Admin")],
        
        "is_superuser": [config("AD_object_Admin"),],
}

AUTH_LDAP_ALWAYS_UPDATE_USER = True
AUTH_LDAP_FIND_GROUP_PERMS = True
AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_CACHE_TIMEOUT = 3600

# AUTH_LDAP_MIRROR_GROUPS = True  # Will sync ldap groups to django, if not exist
# AUTH_LDAP_MIRROR_GROUPS_EXCEPT except some groups we don't want to mirror in django

# AUTH_LDAP_PROFILE_ATTR_MAP = {
#         "home_directory": "homeDirectory"
# }

SESSION_COOKIE_AGE = 30 * 24 * 60 * 60      # Время жизни сессии в куках (указывается в секундах 30 дней)
# также можно настроить куки-name (название куки, в которой будет хранится ключ сессии) 
# и истечение сессии при закрытии браузера (по умолчанию false)

AUTHENTICATION_BACKENDS = (
        'django_auth_ldap.backend.LDAPBackend',
        'django.contrib.auth.backends.ModelBackend',

        ## 'django_remote_auth_ldap.backend.RemoteUserLDAPBackend',
)

DRAL_CHECK_DOMAIN = False

## AUTH_LDAP_CONNECTION_OPTIONS = { ldap.OPT_REFERRALS: 0}

INTERNAL_IPS = [
    config("HOST_IP"), 
    '127.0.0.1'
    ]