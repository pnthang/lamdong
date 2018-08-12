import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

_basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_object('fms.settings.local')

from fms.apps.core.views import main_blueprint
app.register_blueprint(main_blueprint)

from fms.apps.users.views import user_blueprint
app.register_blueprint(user_blueprint, url_prefix="/api/v1")

