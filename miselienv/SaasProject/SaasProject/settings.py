"""
Django settings for SaasProject project.

Generated by 'django-admin startproject' using Django 4.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path


from django.db.models import CASCADE, PROTECT, SET_DEFAULT, SET_NULL, DO_NOTHING


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-qzed!zl0^9ev88_vqa_kns-gyb3==gvk6a@y$20%@b1vceq5h('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
# ALLOWED_HOSTS = ['143.198.163.11', '.localhost', 'localhost', '0.0.0.0', '127.0.0.1']

# Application definition

# todo para tener en cuenta, cuando una app esta en shared_apps y NO esta en tenant_apps,
# todo es ahi cuando es compartido realmente, ahora si la misma app esta en ambos lados, entonces
# todo tanto public como tenants tienen su propias tablas.
SHARED_APPS = (
    'django_tenants',  # mandatory
    'aplicaciones.clientessaas',  # you must list the app where your tenant model resides in

    'django.contrib.contenttypes',

    'aplicaciones.shared_apps',
    'core',
    'aplicaciones.base',
    'aplicaciones.compras',
    'aplicaciones.finanzas',
    'aplicaciones.maquetaweb',
    'aplicaciones.rrhh',
    'aplicaciones.servicios',
    'aplicaciones.stock',
    'aplicaciones.ventas',

    # everything below here is optional
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'import_export',

    'django.contrib.staticfiles',

    'django.contrib.humanize',
    'rest_framework',
    'rest_framework.authtoken',


)

TENANT_APPS = (
    # The following Django contrib apps must be in TENANT_APPS
    'django.contrib.contenttypes',
    # everything below here is optional
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'import_export',

    'django.contrib.staticfiles',

    'django.contrib.humanize',
    'rest_framework',
    'rest_framework.authtoken',

    # your tenant-specific apps
    'core',
    'aplicaciones.base',
    'aplicaciones.compras',
    'aplicaciones.finanzas',
    'aplicaciones.maquetaweb',
    'aplicaciones.rrhh',
    'aplicaciones.servicios',
    'aplicaciones.stock',
    'aplicaciones.ventas',
)

INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]

TENANT_MODEL = "clientessaas.Client"  # app.Model

TENANT_DOMAIN_MODEL = "clientessaas.Domain"  # app.Model

SHOW_PUBLIC_IF_NO_TENANT_FOUND = True

SITE_ID = 1

MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',  # AGREGADO PARA TENANTS
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SaasProject.urls'
PUBLIC_SCHEMA_URLCONF = 'SaasProject.urls_public'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['../templates', './core/templates', '/aplicaciones/ventas/templates'],
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

WSGI_APPLICATION = 'SaasProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': 'saasdb',
        'USER': 'postgres',
        'PASSWORD': '123',
        'HOST': 'localhost',
        'PORT': '',
        # ..
    }
}

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'America/Asuncion'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
# STATIC_ROOT = '/saasdir/static'

# print("aqui hay algo-->", STATICFILES_DIRS, "APCA TAMBIEN-->", BASE_DIR)

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Redirect to home URL after login (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = '/'


# Global Action Foreign Key on delete, must be a DB SS
DB_ON_DELETE_TRANS = PROTECT
DB_ON_DELETE_REC = CASCADE

USE_THOUSAND_SEPARATOR = True

AUTH_USER_MODEL = 'base.UserProfile'

# HTTPS SETTINGS
# https://www.youtube.com/watch?v=mAeK4Ia4fk8 --> para habilitar SSL
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False

# HSTS SETTINGS
SECURE_HSTS_SECONDS = 0  # 518400 equivale a (6 días) # https://stackoverflow.com/questions/49166768/setting-secure-hsts-seconds-can-irreversibly-break-your-site
SECURE_HSTS_PRELOAD = False
SECURE_HSTS_INCLUDE_SUBDOMAINS = False

# esta ultima linea validar posteriormente

# REST_FRAMEWORK = {
#    'DEFAULT_PARSER_CLASSES': (
#        'rest_framework.parsers.JSONParser',
#        'rest_framework.parsers.FormParser',
#    )
#}
