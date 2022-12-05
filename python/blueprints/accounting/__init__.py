from flask import Blueprint

accounting = Blueprint('accounting', __name__, template_folder='templates', static_folder='static')
from . import routes
