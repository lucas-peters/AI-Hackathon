from flask import Flask
import os

def create_app():
    template_dir = os.path.abspath('../../frontend/src')
    app = Flask(__name__, template_folder=template_dir)
    app.config['SECRET_KEY'] = 'verysecurekey'
    
    from .views import views
    app.register_blueprint(views)
    return app
    