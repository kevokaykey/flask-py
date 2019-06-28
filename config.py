"""ENV configs module"""
import os


class Base(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    USER = os.getenv('USER')
    PASSWORD = os.getenv('PASSWORD')
    HOST = os.getenv('localhost')


class Development(Base):
    """Development configurations."""
    DEBUG =True
    DATABASE = os.getenv('DEV_DATABASE')


class Testing(Base):
    """Configurations for Testing."""
    TESTING = True
    DEBUG = True
    DATABASE = os.getenv('TEST_DATABASE')


class Production(Base):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'secretkey123'


