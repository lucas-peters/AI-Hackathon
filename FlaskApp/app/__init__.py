from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
import os


def create_app():
    template_dir = os.path.abspath('../../frontend/src')
    app = Flask(__name__, template_folder=template_dir)
    cors = CORS(app,resources={r"/*": {"origins": "*"}})
    app.config['SECRET_KEY'] = 'KL06xVMcnZpUmnTZemJ0kivJpvDNgWig'
    app.config['JWT_SECRET_KEY'] = '67RagpLnpshZebfmsBW0Ya9mNZfP9QaV'  # Change this to a strong key
    app.config['CORS_HEADERS'] = 'Content-Type'
    jwt = JWTManager(app)
    
    from .chat import chat
    from .auth import auth
    app.register_blueprint(chat)
    app.register_blueprint(auth)
    
    return app
    