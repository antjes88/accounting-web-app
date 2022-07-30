# general libraries
from flask import redirect, url_for, render_template, session
from flask_login import current_user, login_user, login_required, logout_user, LoginManager
from datetime import timedelta

# calling to own files
from . import globals_login
from .models import get_user, get_users_db
from .forms import *


def login_page_routing(login_page, home_page_path):
    @login_page.route('/login_page', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for(home_page_path))
        form = LoginForm()
        globals_login.users = []
        get_users_db()
        if form.validate_on_submit():
            user = get_user(form.email.data)
            if user is not None and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for(home_page_path))
        return render_template('login_page/login_form.html', form=form)

    @login_page.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login_page.login'))


def login_manager_definition(application):
    login_manager = LoginManager()
    login_manager.init_app(application)
    login_manager.login_view = "login_page.login"

    @login_manager.user_loader
    def load_user(user_id):
        for user in globals_login.users:
            if int(user.id) == int(user_id):
                return user
        return None

    @application.before_request
    def make_session_permanent():
        session.permanent = True
        application.permanent_session_lifetime = timedelta(seconds=301)
