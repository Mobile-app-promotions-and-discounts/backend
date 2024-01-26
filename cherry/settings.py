import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get('DEBUG', False) == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(', ')

AUTH_USER_MODEL = 'users.User'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'rest_framework',
    'rest_framework_simplejwt',
    'djoser',
    'django_filters',
    'api',
    'users',
    'parsing_stores',
    'products',
    'drf_yasg',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cherry.urls'

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

WSGI_APPLICATION = 'cherry.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE'),
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}

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

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

DJOSER = {
    'TOKEN_MODEL': None,
    'SERIALIZERS': {
        'user_create': 'api.serializers.CustomUserCreateSerializer',
        'user': 'api.serializers.CustomUserSerializer',
        'current_user': 'api.serializers.CustomUserSerializer',
    },
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer',),
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
}

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR.joinpath('static')

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.joinpath('media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGER_MAGNIT = {
    'version': 1,
    'formatters': {
        'consoleFormatter': {
            'format': '%(asctime)s - %(name)s - %(levelname)-8s - %(message)s - [* %(filename)s:%(lineno)d *]',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'fileFormatter': {
            'format': '%(asctime)s - %(name)s - %(levelname)-8s - %(message)s - [* %(filename)s:%(lineno)d *]',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'consoleHandler': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'consoleFormatter',
            'stream': 'ext://sys.stdout',
        },
        'fileHandler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'fileFormatter',
            'filename': 'parser_magnit.log',
            'maxBytes': 52428800,
            'backupCount': 3,
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': [
            'consoleHandler',
            'fileHandler',
        ],
    },
}

PARSING_MAGNIT = {
    'URL_PRODUCTS': 'https://web-gateway.middle-api.magnit.ru/v1/promotions',
    'URL_CITY': 'https://web-gateway.middle-api.magnit.ru/v1/cities',
    'URL_STORES': 'https://web-gateway.middle-api.magnit.ru/v1/geolocation/store',
    'HEADERS': {
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Origin': 'https://magnit.ru',
        'Referer': 'https://magnit.ru/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                    'Chrome/119.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'x-app-version': '0.1.0',
        'x-client-name': 'magnit',
        'x-device-id': 'v66jbingss',
        'x-device-platform': 'Web',
        'x-device-tag': 'disabled',
        'x-platform-version': 'window.navigator.userAgent',
    },
    'PARAMS_PRODUCTS': {
        'offset': '0',
        'limit': '1',
        'storeId': '63452',
        'adult': 'true',
        'sortBy': 'priority',
        'order': 'desc',
    },
    'PARAMS_STORES': {
        'Limit': 3,
        'Radius': 20,
    },
    # Распределение категорий "Магнит" по категориям приложения
    'CATEGORIES': {
        'PRODUCTS': [
            'Хлеб и выпечка',
            'Овощи и фрукты',
            'Молоко, сыр, яйца',
            'Мясо, птица, колбасы',
            'Замороженные продукты',
            'Напитки',
            'Готовая еда',
            'Чай, кофе, какао',
            'Бакалея, соусы',
            'Кондитерские изделия',
            'Снеки, орехи',
            'Соусы и приправы',
            'Здоровое питание',
            'Рыба и морепродукты',
            'Готовая еда',
        ],
        'CLOTHES': [
            'Одежда и обувь',
        ],
        'HOME': [
            'Дом, сад',
            'Медтовары',
            'Бытовая техника',
            'Бытовая химия',
            'Скидки по карте',
            'Новинки',
            'Досуг',
            'Канцтовары',
            'Витамины и БАД',
            'Аксессуары',
            'Лекарства',
            'Печатная продукция',
        ],
        'COSMETICS': [
            'Косметика и парфюмерия',
            'Гигиена',
        ],
        'KIDS': [
            'Детям',
        ],
        'ZOO': [
            'Зоотовары',
        ],
        'AUTO:': ['Автотовары'],
        'HOLIDAYS': [
            'Алкоголь',
            'Новый год',
        ],
        'DIFFERENT': [
            'Скидки по карте',
            'Скидки на категории',
            '30% бонусами с подпиской',
            'Новинки',
            'Кешбек',
            'Разные категории',
            '0',
            'Проездные. Лотереи',
        ],
    },
    'NO_DATA': -1,
}


REDIS_HOST = os.environ.get('REDIS_SRC_HOST', 'redis_src')
REDIS_PORT = os.environ.get('REDIS_SRC_PORT', '6379')
CELERY_BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_IMPORTS = ('parsing_stores.tasks',)
CELERY_TIMEZONE = 'Europe/Moscow'
