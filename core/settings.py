from starlette.config import Config
import os
from core.utils import load_models

config = Config('.env')

HOSTNAME = config('HOSTNAME', cast=str, default="localhost")
PORT = config('PORT', cast=int, default=8080)
DEBUG = config('DEBUG', cast=bool, default=True)

TIMEZONE = config('DEBUG', cast=str, default='UTC')
USE_TIMEZONE = config('USE_TIMEZONE', cast=bool, default=False)

ALLOWED_HOSTS = ["http://localhost", "http://localhost:8080"]

DATABASE = {
    "mysql" : {
        "engine" : "tortoise.backends.mysql",
        "credentials": {
            "host" : config("DB_HOST", cast=str, default='172.17.0.2'),
            "database": config("DB_NAME", cast=str, default="ecommercedevdb"),
            "port": config("DB_PORT", cast=int, default=3306),
            "user": config("DB_USER", cast=str, default="root"),
            "password": config("DB_PASSWORD", cast=str, default="123456") 
        },
    },
    #"sqlite": "sqlite://db.sqlite3"
}

TORTOISE_ORM = {
    "connections" : {
        "default" : DATABASE[config("DB_ENGINE", cast=str, default="mysql")]
    },

    "apps": {
        "models":{
            "models": [*load_models(), "aerich.models"],
            "default_connection" : "default"
        }
    },

    "use_tz": USE_TIMEZONE,
    "timezone": TIMEZONE
}

SECRET_KEY = config("SECRET_KEY", cast=str, default="mybest-secret-key")
JWT_TOKEN_ALGORITHM = config("JWT_TOKEN_ALGORITHM", cast=str, default='HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=90)

AWS_ACCESS_KEY_ID =  os.environ.get('AWS_ACCESS_KEY_ID', '123456')
AWS_SECRET_ACCESS_KEY=  os.environ.get('AWS_SECRET_ACCESS_KEY', '123456')
AWS_REGION =  os.environ.get('AWS_REGION', 'us-east-1')
S3_BUCKET_NAME =  os.environ.get('S3_BUCKET_NAME', 's3bucket')

AUTH_URL = config("AUTH_URL", cast=str, default="auth/login")

MAIL_USERNAME = config('MAIL_USERNAME', cast=str, default='8504c1ffbcd79a')
MAIL_PASSWORD = config('MAIL_PASSWORD', cast=str, default='d25828b56b032f')
MAIL_FROM = config('MAIL_FROM', cast=str, default='canow712@gmail.com')
MAIL_PORT = config('MAIL_PORT', cast=int, default=2525)
MAIL_SERVER = config('MAIL_SERVER', cast=str, default='smtp.mailtrap.io')
MAIL_FROM_NAME = config('MAIL_FROM_NAME', cast=str,  default='FastAPI')
MAIL_USE_TLS = config('MAIL_USE_TLS', cast=bool, default=True)
MAIL_USE_SSL = config('MAIL_USE_SSL', cast=bool, default=False)
MAIL_USE_CREDENTIALS = config('MAIL_USE_CREDENTIALS',cast=bool, default=True)
MAIL_VALIDATE_CERTS = config('MAIL_VALIDATE_CERTS', cast=bool, default=False)


# Celery and redis settings
CELERY_BROKER_URL = config(
    'CELERY_BROKER_URL', cast=str, default='redis://172.17.0.4:6379')
CELERY_RESULT_BACKEND = config(
    'CELERY_RESULT_BACKEND', cast=str, default='redis://172.17.0.4:6379')
CELERY_TASKS_REGISTER = [
    # ','.join(load_tasks()) # import automatically tasks
    'tasks.users'
]