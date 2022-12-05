# public libraries
from flask import Flask

# load env variables
from CommonResources.Classes.common_resources import *

Miscellaneous.env_var_loader('.env')

# importing blueprints and dashes
from blueprints.login import login_blueprint
from blueprints.home import home_page
from blueprints.accounting import accounting

# flask app creation
application = Flask(__name__)

# secret key definition
application.config['SECRET_KEY'] = os.environ['SECRET_KEY']

# adding blueprints
application.register_blueprint(login_blueprint(application, 'home_page.home'))
application.register_blueprint(home_page)
application.register_blueprint(accounting)
