from flask import Flask


from config import Config
from application.extensions import db, migrate, googlemaps, bcrypt, login_manager, csrf



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    #Initialising Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    googlemaps.init_app(app)
    bcrypt.init_app(app)

    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login_functionality.login'
    login_manager.needs_refresh_message_category = "danger"
    login_manager.login_message = u"Please login first"

    # Registering blueprints
    from application.admin import bp as admin_bp
    from application.login_functionality import bp as login_functionality_bp
    from application.public import bp as public_bp
    from application.users import bp as user_bp

    app.register_blueprint(admin_bp)
    app.register_blueprint(login_functionality_bp)
    app.register_blueprint(public_bp)
    app.register_blueprint(user_bp)

    return app
