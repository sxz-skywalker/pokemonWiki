import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret')
    DEBUG = True
    DATABASE_HOST = os.environ.get('DATABASE_HOST')
    DATABASE_USER = os.environ.get('DATABASE_USER')
    DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
    DATABASE_SCHEMA = os.environ.get('DATABASE_SCHEMA')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')


config = Config()
