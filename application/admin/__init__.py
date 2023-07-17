import flask

bp = flask.Blueprint('admin', __name__, url_prefix="/admin")

from application.admin import routes