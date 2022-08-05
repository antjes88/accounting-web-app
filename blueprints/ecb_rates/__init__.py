from flask import Blueprint

ecb_rates = Blueprint('ecb_rates', __name__, template_folder='templates', static_folder='static')
from . import routes
