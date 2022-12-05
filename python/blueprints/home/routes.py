# public libraries
from flask import render_template, request
from flask_login import login_required

# own files
from . import home_page


@home_page.route("/")
@login_required
def home():
    """
    Landing route for Web App

    Returns: renders home_page/home.html
    """
    return render_template('home_page/home.html')


@home_page.route('/successful')
@login_required
def successful():
    """
    Successful route for process successfully executed with the Web App

    Returns: home_page/successful.html with possibility to go back to process to repeat operation
        (url_for(blueprint, go_back_to))
    """
    return render_template(
        'home_page/successful.html', go_back_to=request.args.get('go_back_to'), blueprint=request.args.get('blueprint'))


@home_page.route('/error')
@login_required
def error_page():
    """
    Error route for process execution failures with the Web App

    Returns: home_page/error_page.html and error message from failing process
    """
    return render_template('home_page/error_page.html', message=request.args.get('message'))
