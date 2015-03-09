from flask import Flask

from . import models
from .extensions import config, oauth, assets
from .views.starry import starry
from .views.users import users


DEBUG = True
SECRET_KEY = 'development-key'


def create_app():
    app = Flask(__name__)
    app.config.from_object(__name__)

    config.init_app(app)
    oauth.init_app(app)
    assets.init_app(app)

    app.register_blueprint(starry)
    app.register_blueprint(users)

    return app