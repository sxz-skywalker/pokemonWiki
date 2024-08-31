import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'mysql+pymysql://root:password@db/pokemon_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret')
    DEBUG = True
    DATABASE_HOST = os.environ.get('DATABASE_HOST')
    DATABASE_USER = os.environ.get('DATABASE_USER')
    DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
    DATABASE_SCHEMA = os.environ.get('DATABASE_SCHEMA')


config = Config()
