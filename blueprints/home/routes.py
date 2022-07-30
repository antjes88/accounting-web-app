# public libraries
from flask import render_template, request
from flask_login import login_required
import os

# own files
from . import home_page


@home_page.route("/")
@login_required
def home():
    return render_template('home_page/home.html')


@home_page.route('/successful')
@login_required
def successful():
    go_back_to = request.args.get('go_back_to')
    blueprint = request.args.get('blueprint')

    return render_template('home_page/successful.html', go_back_to=go_back_to, blueprint=blueprint)


@home_page.route('/error')
@login_required
def error_page():
    message = request.args.get('message')

    return render_template('home_page/error_page.html', message=message)
