from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from meetup_app_flask.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from meetup_app_flask import routes, models
