from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask import Flask

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    from . import config
    app = Flask(__name__)
    app.secret_key = config.SECRET_KEY
    app.config.from_object(config)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from .models.user import user1
    from .models.event import event1
    from .models.booking import booking1

    from .routes.auth_routes import auth_bp
    from .routes.event_routes import event_bp
    from .routes.booking_routes import booking_bp
    from .routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(event_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(admin_bp)

    return app

__all__ = ["db", "bcrypt", "jwt", "create_app"]




