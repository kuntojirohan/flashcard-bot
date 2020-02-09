from app import routes, models
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


def _update_db(obj):
    """
    Method used for updating the db with the data object input
    """
    db.session.add(obj)
    db.session.commit()
    return obj


# this line is added at the bottom to avoid circular dependencies when starting the Flask server
# Both the routes.py and models.py files require the app and db objects to
# be instantiated before the entire file can be loaded by Flask correctly
