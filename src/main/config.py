import os
from typing import Callable, Any

import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
SQLALCHEMY_TRACK_MODIFICATIONS = False
MAIL_SERVER = os.environ.get('MAIL_SERVER')
MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
PASSWORD_RESET_TOKEN_USE = os.environ.get('PASSWORD_RESET_TOKEN_USE')
ACCOUNT_ACTIVATION_TOKEN_USE = os.environ.get('ACCOUNT_ACTIVATION_TOKEN_USE')
PASSWORD_RESET_EMAIL_SUBJECT = os.environ.get('PASSWORD_RESET_SUBJECT')
ACCOUNT_ACTIVATION_EMAIL_SUBJECT = os.environ.get('ACCOUNT_ACTIVATION_SUBJECT')


def get_db():
    connection = psycopg2.connect(
        database="simba_db",
        user="simba",
        password='Yuta&"DmYj{eFIm[',
        host="35.246.25.244",
        port=5432,
        cursor_factory=RealDictCursor,
    )

    return lambda: connection


def close_db(db: Callable[[], Any], e=None):
    if db is not None:
        db().close()
