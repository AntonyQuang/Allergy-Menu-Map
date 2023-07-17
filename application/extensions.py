from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_googlemaps import GoogleMaps, Map
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect


db = SQLAlchemy()
migrate = Migrate()
googlemaps = GoogleMaps()
bcrypt = Bcrypt()
login_manager = LoginManager()
csrf = CSRFProtect()