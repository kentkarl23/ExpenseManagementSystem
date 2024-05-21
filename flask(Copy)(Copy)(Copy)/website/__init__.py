from flask import Flask
from .auth import auth
from .views import views
from .xml_utils import create_users_xml, create_transactions_xml
import os
from flask_login import LoginManager
from .models import User

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['STATIC_FOLDER'] = 'data'
    
    # Create an instance of LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Check if XML files exist, and create them if they don't
    if not os.path.exists('users.xml'):
        create_users_xml()

    if not os.path.exists('transactions.xml'):
        create_transactions_xml()

    # Register the auth blueprint
    app.register_blueprint(auth)
    app.register_blueprint(views)

    @login_manager.user_loader
    def load_user(user_id):
        # Load user from XML file using the custom method defined in the User class
        return User.get_by_id(user_id)

    return app