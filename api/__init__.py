##############################
######### IMPORTS ############
##############################

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import DevelopmentConfig, config

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db = SQLAlchemy(app)
mig = Migrate()

def create_app(config_name):

    app.config.from_object(config[config_name])

    db.init_app(app)

    mig.init_app(app, db)


    ##############################################################
    ################ REGISTERING VIEWS ###########################
    ##############################################################

    from api.routes import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app