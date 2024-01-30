# app/config.py

class Config:
    JWT_SECRET_KEY = "artemons"
    SECRET_KEY = 'artemons'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///artemons.db'
    DEBUG = False
    TESTING = False
    DEVELOPMENT = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True


class ConfigDebug(Config):
    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    WTF_CSRF_ENABLED = False


class ConfigTesting(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
    WTF_CSRF_ENABLED = False
