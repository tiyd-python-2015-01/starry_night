from flask import Flask

from . import models
from .extensions import config, assets
from .views.starry import starry
from .views.github import github_blueprint


DEBUG = True
SECRET_KEY = 'development-key'


def create_app():
    app = Flask(__name__)
    app.config.from_object(__name__)

    config.init_app(app)
    assets.init_app(app)

    app.register_blueprint(starry)
    # github_blueprint.load_config()
    app.register_blueprint(github_blueprint, url_prefix="/login")

    return app