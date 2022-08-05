from flask_login import UserMixin
from werkzeug.security import check_password_hash
from blueprints.login import globals_login
from CommonResources.Classes.common_resources import *


class User(UserMixin):
    """
    Implementation of UserMixin to handle login/logout with flask_login

    Args:
         user_id: user id
         user_name: login username
         user_password: password for authentication of user. It is the hash value. To create password
            use generate_password_hash()
        is_admin: if the user is admin, by default is False
    """
    def __init__(self, user_id, user_name, user_password, is_admin=False):
        self.id = user_id
        self.user_name = user_name
        self.password = user_password
        self.is_admin = is_admin

    def check_password(self, password):
        """
        Method to evaluate if the user_password submitted is the one to authenticate the user.
        Method wrappers check_password_hash()
        Args:
            password: user_password submitted by user trying to authenticate

        Returns:
            - True if the user_password is the right one
            - False if it is not
        """
        return check_password_hash(self.password, password)  # to create user_password generate_password_hash

    def __repr__(self):
        return '<User {}>'.format(self.user_name)


def get_user(user_name):
    """
    Look for user with user_name in globals_login.users

    Args:
        user_name: name of user to look for

    Returns:
        - If user_name is found in globals_login.users, it returns instance of User
        - If user_name is not found in globals_login.users, returns None
    """
    for user in globals_login.users:
        if user.user_name == user_name:
            return user
    return None


def load_globals_login_users():
    """
    Load authenticator user as instances of User class into globals_login.users from environment variables.
    It can be modified to look for users detail from other sources (e.g. a db)

    Returns: saves on variable globals_login.users an instance of class User with
        the data extracted from environment variables
    """
    user_already_loaded = False
    for user in globals_login.users:
        if 1 == user.id:
            user_already_loaded = True

    if not user_already_loaded:
        globals_login.users.append(
            User(1, os.environ['USER'], os.environ['PASSWORD'])
        )
