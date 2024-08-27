from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
    app.config['SECRET_KEY'] = 'randomSecretKey'

    db.init_app(app)
    bcrypt.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from app.routes.auth_routes import auth_bp
    from app.routes.product_routes import product_bp
    from app.routes.ticket_routes import ticket_bp
    from app.routes.cart_routes import cart_bp
    from app.routes.section_routes import section_bp
    from app.routes.dashboard_routes import dashboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(ticket_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(section_bp)
    app.register_blueprint(dashboard_bp)

    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models.userModel import UserModel
    return UserModel.query.get(int(user_id))
