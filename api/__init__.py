##############################
######### IMPORTS ############
##############################

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import config, ProductionConfig

# APP CONFIG
app = Flask(__name__)
app.config.from_object(ProductionConfig)
db = SQLAlchemy(app)
mig = Migrate()

def create_app(config_name):

    # INIT APP CONFiG IN APP
    app.config.from_object(config[config_name])

    # INIT EXTERNAL MODULES
    db.init_app(app)
    mig.init_app(app, db)

    # REGISTER BLUEPRINTS

    from api.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app