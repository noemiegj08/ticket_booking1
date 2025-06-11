from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask import Flask

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    from app.config import Config
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate = Migrate(app, db)

    from app.models.user import user1
    from app.models.event import event1
    from app.models.booking import booking1

    from app.routes.auth_routes import auth_bp
    from app.routes.event_routes import event_bp
    from app.routes.booking_routes import booking_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(event_bp)
    app.register_blueprint(booking_bp)

    from app.routes.admin_routes import admin_bp
    app.register_blueprint(admin_bp)

    import jwt as pyjwt

    @app.template_filter("decode_jwt")
    def decode_jwt(token):
        try:
            return pyjwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        except:
            return {}

    return app

__all__ = ["db", "bcrypt", "jwt", "create_app"]
