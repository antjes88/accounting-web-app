from flask import Blueprint
from .routes import *


def login_blueprint(application, home_page_path):
    """
    Wrapper for login blueprint.

    Args:
        application: flask application to apply login protection
        home_page_path: path to application landing page
    Returns: login blueprint
    """
    login_page = Blueprint('login_page', __name__, template_folder='templates', static_folder='static')
    login_page_routing(login_page, home_page_path)
    login_manager_definition(application)

    return login_page
