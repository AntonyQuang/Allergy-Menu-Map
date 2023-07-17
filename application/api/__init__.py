import flask

bp = flask.Blueprint('api', __name__, url_prefix="/api")

from application.api import routes
