from flask import Flask
from flask_login import LoginManager
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os

login_manager = LoginManager()


def create_app():
    template_dir = os.path.abspath('../../frontend/src')
    app = Flask(__name__, template_folder=template_dir)
    app.config['SECRET_KEY'] = 'verysecurekey'
    app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Change this to a strong key
    jwt = JWTManager(app)
    login_manager.init_app(app)
    
    from .views import views
    app.register_blueprint(views)
    return app
    