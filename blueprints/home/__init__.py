from flask import Blueprint

home_page = Blueprint('home_page', __name__, template_folder='templates', static_folder='static')
from . import routes