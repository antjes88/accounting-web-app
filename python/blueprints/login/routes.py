# general libraries
from flask import redirect, url_for, render_template, session
from flask_login import current_user, login_user, login_required, logout_user, LoginManager
from datetime import timedelta

# calling to own files
from . import globals_login
from .models import get_user, load_globals_login_users
from .forms import *


def login_page_routing(login_page, home_page_path):
    """
    Wrapper to create routes for login & log_out for the login blueprint

    Args:
        login_page: self reference to own login blueprint to add routes
        home_page_path: route to landing page by default
    Returns: creation of routes for login & log_out for the login blueprint provided (login_page)
    """
    @login_page.route('/login_page', methods=['GET', 'POST'])
    def login():
        """
        Login route.

        Returns:
            - For user already authenticated returns home_page_path
            - For correct authentication returns home_page_path
            - For wrong authentication returns login_page/login_form.html (login)
            - For no authenticated user returns login_page/login_form.html (login)
        """
        if current_user.is_authenticated:
            return redirect(url_for(home_page_path))

        form = LoginForm()
        globals_login.users = []
        load_globals_login_users()
        if form.validate_on_submit():
            user = get_user(form.user_name.data)
            if user is not None and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)

                return redirect(url_for(home_page_path))

        return render_template('login_page/login_form.html', form=form)

    @login_page.route('/logout')
    @login_required
    def logout():
        """
        logout route.

        Returns: close user session and redirect to login_page.login
        """
        logout_user()

        return redirect(url_for('login_page.login'))


def login_manager_definition(application):
    """
    Function to instantiate Login Manager for the flask application provided (application).
    This allows to set settings used for logging in.

    Args:
        application: flask application to apply LoginManager
    Returns: This allows to set settings used for logging in:
        - login_manager.login_view = "login_page.login": when a user attempts to access a route protected with
            login_required without being logged in, Flask-Login will redirect them to the log in view.
        - load_user is implemented to use the class User: This callback is used to reload the user object from
            the user ID stored in the session
        - makes session permanent and extends lifetime of session for 301 seconds
    """
    login_manager = LoginManager()
    login_manager.init_app(application)
    login_manager.login_view = "login_page.login"

    @login_manager.user_loader
    def load_user(user_id):
        """
        Callback used to reload the user object from the user ID stored in the session
        Args:
            user_id: it is str, user ID stored in the session

        Returns:
            - None if id is not valid
            - user object if the id is valid
        """
        for user in globals_login.users:
            if int(user.id) == int(user_id):
                return user
        return None

    @application.before_request
    def make_session_permanent():
        """
        Function that makes session permanent and extends lifetime of session for 301 seconds
        """
        session.permanent = True
        application.permanent_session_lifetime = timedelta(seconds=301)
