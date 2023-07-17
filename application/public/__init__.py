import flask

bp = flask.Blueprint('public', __name__)

from application.public import routes