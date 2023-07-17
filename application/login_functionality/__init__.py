import flask

bp = flask.Blueprint('login_functionality', __name__, url_prefix="/login")

from application.login_functionality import routes