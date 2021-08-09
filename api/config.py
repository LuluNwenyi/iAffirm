##############################
######### IMPORTS ############
##############################


import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():

    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    @staticmethod
    def init_app():
        pass

###### DEV CONFIG #######
#########################

class DevelopmentConfig(Config):

    DEBUG = True 
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') 


###### TEST CONFIG #######
##########################

class TestingConfig(Config):

    TESTING = True 
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


###### PRODUCTION CONFIG #######
################################

class ProductionConfig(Config):

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


#ENV CONFiG

config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
    }
