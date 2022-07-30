from flask_login import UserMixin
from werkzeug.security import check_password_hash
from blueprints.login import globals_login
from CommonResources.Classes.common_resources import *


class User(UserMixin):
    def __init__(self, df, is_admin=False):
        self.id = df['Id']
        self.email = df['UserEmail']
        self.password = df['Password']
        self.is_admin = is_admin

    def check_password(self, password):
        return check_password_hash(self.password, password)  # to create password generate_password_hash

    def __repr__(self):
        return '<User {}>'.format(self.email)


def get_user(email):
    for user in globals_login.users:
        if user.email == email:
            return user
    return None


# Creation of users
def get_users_db():
    my_dict = {'Id': [1], 'UserEmail': [os.environ['USER']], 'Password': [os.environ['PASSWORD']]}
    log_df = pd.DataFrame.from_dict(my_dict, orient='columns')
    for x in log_df.index:
        globals_login.users.append(User(log_df.loc[x]))
