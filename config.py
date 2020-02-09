import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
    Contains all the config details to connect with the SQLite database
    """
    DEBUG = False
    TESTING = False
    SECRET_KEY = "my-sample-secret-key-for-wbot-databse"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False