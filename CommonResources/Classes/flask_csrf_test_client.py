# THIS SOLUTION IS BASED ON THIS ONE https://gist.github.com/singingwolfboy/2fca1de64950d5dfed72
import flask
from flask.testing import FlaskClient as BaseFlaskClient
from flask_wtf.csrf import generate_csrf


class RequestShim(object):
    """
    A fake request that proxies cookie-related methods to a Flask test client.
    Flask's assumptions about an incoming request do not match up with what the test client provides in terms of
    manipulating cookies, and the CSRF system depends on cookies working correctly.

    Args:
        client: flask client
    """
    def __init__(self, client):
        self.client = client
        self.vary = set({})

    def set_cookie(self, key, value='', *args, **kwargs):
        """
        Set the cookie on the Flask test client.
        """
        server_name = flask.current_app.config["SERVER_NAME"] or "localhost"

        return self.client.set_cookie(server_name, key=key, value=value, *args, **kwargs)

    def delete_cookie(self, key, *args, **kwargs):
        """
        Delete the cookie on the Flask test client
        """
        server_name = flask.current_app.config["SERVER_NAME"] or "localhost"

        return self.client.delete_cookie(server_name, key=key, *args, **kwargs)


class TestFlaskClient(BaseFlaskClient):
    """
    Extension to Flask's built-in test client class that knows how to look up CSRF tokens.
    Using this class, Flask applications can be tested with CSRF protections turned on, to make sure that CSRF
    works properly in production as well. It means that you can test your application with user authentication
    activated.
    *A CSRF token is a secure random token (e.g., synchronizer token or challenge token) that is used to prevent
    CSRF attacks. The token needs to be unique per user session and should be of large random value to make it
    difficult to guess. A CSRF secure application assigns a unique CSRF token for every user session.
    """
    def __init__(self, *args, **kwargs):
        super(TestFlaskClient, self).__init__(*args, **kwargs)
        self.login_url = None
        self.password = None
        self.username = None
        self.csrf_token = None

    def setup(self, password, username, login_route):
        """
        Method to set values to object parameters. This is the entry point to the class. It is necessary because the
        class has to be instantiated by the application itself.

        Args:
            login_route: the endpoint of the application login page (name of the function)
            username: name of the user to authenticate
            password: password of the user to authenticate
        """
        self.password = password
        self.username = username
        self.login_url = self.find_url_from_route(login_route)

    def csrf_token_creator(self):
        """
        Creates csrf token for user session
        """
        request = RequestShim(self)
        environ_overrides = {}
        self.cookie_jar.inject_wsgi(environ_overrides)

        with self.application.app_context():
            with flask.current_app.test_request_context(self.login_url, environ_overrides=environ_overrides):
                self.csrf_token = generate_csrf()
                self.application.session_interface.save_session(self.application, flask.session, request)

    def find_url_from_route(self, route):
        """
        Method that returns url assigned to a route.

        Args:
            route: the endpoint of the URL (name of the function)
        Returns: url for a route
        """
        with self.application.app_context():
            return flask.url_for(route)

    def login(self):
        """
        Method to authenticate the user provided.

        Returns: redirection to login for user provided.
        """
        self.csrf_token_creator()

        return self.post(self.login_url, data={
            "user_name": self.username,
            "password": self.password,
            "csrf_token": self.csrf_token,
        }, follow_redirects=True)

    def logout(self, logout_route):
        """
        Method to log out an authenticated user.

        Args:
            logout_route: the endpoint of the application logout page (name of the function)
        Returns: redirection to login page.
        """
        return self.get(self.find_url_from_route(logout_route), follow_redirects=True)

    def get_with_login(self, redirect_to_route, query_string=None, follow_redirects=False):
        """
        Method that authenticates the user instantiated and does a get request to the application

        Args:
            redirect_to_route: the endpoint of the application url to send get request (name of the function)
            query_string: an optional string or dict with URL parameters.
            follow_redirects: Set this to True if the Client should follow HTTP redirects.
        Returns: redirection to login for user provided.
        """
        self.login()

        return self.get(self.find_url_from_route(redirect_to_route),
                        query_string=query_string,
                        follow_redirects=follow_redirects)

    def post_with_login(self, redirect_to_route, data, follow_redirects=False):
        """
        Method that authenticates the user instantiated and does a post request to the application

        Args:
            redirect_to_route: the endpoint of the application url to send post request (name of the function)
            data: a string or dict of form data or a file-object.
            follow_redirects: Set this to True if the Client should follow HTTP redirects.
        Returns: redirection to login for user provided.
        """
        self.login()
        data['csrf_token'] = self.csrf_token

        return self.post(self.find_url_from_route(redirect_to_route), data=data, follow_redirects=follow_redirects)
