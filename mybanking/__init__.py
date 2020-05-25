import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from config import app_config


db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    Bootstrap(app)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)

    return app


config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)
ma = Marshmallow(app)
migrate = Migrate(app, db)

from mybanking import routes
