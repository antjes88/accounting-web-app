# public libraries
from flask import Flask
# import dash

# load env variables
from CommonResources.Classes.common_resources import *

Miscellaneous.env_var_loader('env/.env')

# importing blueprints and dashes
from blueprints.login import login_blueprint
from blueprints.ecb_rates import ecb_rates
from blueprints.home import home_page

# flask app creation
application = Flask(__name__)

# secret key definition
application.config['SECRET_KEY'] = os.environ['SECRET_KEY']

# adding blueprints
application.register_blueprint(login_blueprint(application, 'home_page.home'))
application.register_blueprint(ecb_rates)
application.register_blueprint(home_page)
