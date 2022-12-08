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
app = Flask(__name__)

# secret key definition
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

# adding blueprints
app.register_blueprint(login_blueprint(app, 'home_page.home'))
app.register_blueprint(home_page)
app.register_blueprint(accounting)
