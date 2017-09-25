# -*- coding: utf-8 -*-
# config.py


class Config(object):
    """
    Common configurations
    """
    WTF_CSRF_ENABLED = True
    WTF_CSRF_CHECK_DEFAULT = True
    WTF_CSRF_METHODS = {'POST', 'PUT', 'PATCH', 'DELETE'}
    WTF_CSRF_HEADERS = ['X-CSRFToken', 'X-CSRF-Token']
    WTF_CSRF_TIME_LIMIT = 3600
    WTF_CSRF_SSL_STRICT = True


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    TESTING = False
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    """
    Testing configurations
    """
    TESTING = True
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    """
    Production configurations
    """
    TESTING = False
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app_config = {'development':  DevelopmentConfig,
              'testing': TestingConfig,
              'production':   ProductionConfig}
