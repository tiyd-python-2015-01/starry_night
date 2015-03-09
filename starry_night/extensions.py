from flask.ext.assets import Environment

assets = Environment()

# Change this to HerokuConfig if using Heroku.
from flask.ext.appconfig import AppConfig

config = AppConfig()
