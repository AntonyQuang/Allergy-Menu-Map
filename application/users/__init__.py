import flask

bp = flask.Blueprint('users', __name__, url_prefix="/users")

from application.users import routes