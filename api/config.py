##############################
######### IMPORTS ############
##############################

import os
import re 
basedir = os.path.abspath(os.path.dirname(__file__))

# BASE CONFiG
class Config():

    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'apikey'
    MAIL_PASSWORD = os.environ.get('SENDGRID_API_KEY')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT')
    
    @staticmethod
    def init_app():
        pass


# DEV CONFiG
class DevelopmentConfig(Config):

    DEBUG = True 
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL')
 

# TEST CONFiG
class TestingConfig(Config):

    TESTING = True 
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL')


# PRODUCTION CONFiG
class ProductionConfig(Config):

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    #if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        #SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

#ENV CONFiG

config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
    }

