# THIS SOLUTION IS BASED ON THIS ONE https://gist.github.com/singingwolfboy/2fca1de64950d5dfed72
import flask
from flask.testing import FlaskClient as BaseFlaskClient
from flask_wtf.csrf import generate_csrf


class RequestShim(object):
    """
    A fake request that proxies cookie-related methods to a Flask test client.
    """
    def __init__(self, client):
        self.client = client
        self.vary = set({})

    def set_cookie(self, key, value='', *args, **kwargs):
        server_name = flask.current_app.config["SERVER_NAME"] or "localhost"

        return self.client.set_cookie(server_name, key=key, value=value, *args, **kwargs)

    def delete_cookie(self, key, *args, **kwargs):
        server_name = flask.current_app.config["SERVER_NAME"] or "localhost"

        return self.client.delete_cookie(server_name, key=key, *args, **kwargs)


class FlaskClient(BaseFlaskClient):
    def __init__(self, *args, **kwargs):
        super(FlaskClient, self).__init__(*args, **kwargs)
        self.login_url = None
        self.password = None
        self.username = None
        self.csrf_token = None

    def setup(self, password, username, login_route):
        self.password = password
        self.username = username
        self.login_url = self.find_url_from_route(login_route)

    def csrf_token_creator(self):
        request = RequestShim(self)
        environ_overrides = {}
        self.cookie_jar.inject_wsgi(environ_overrides)

        with self.application.app_context():
            with flask.current_app.test_request_context(self.login_url, environ_overrides=environ_overrides):
                self.csrf_token = generate_csrf()
                self.application.session_interface.save_session(self.application, flask.session, request)

    def find_url_from_route(self, route):
        with self.application.app_context():
            return flask.url_for(route)

    def login(self):
        self.csrf_token_creator()

        return self.post(self.login_url, data={
            "email": self.username,
            "password": self.password,
            "csrf_token": self.csrf_token,
        }, follow_redirects=True)

    def logout(self, logout_route):
        return self.get(self.find_url_from_route(logout_route), follow_redirects=True)

    def get_with_login(self, redirect_to_route, query_string=None, follow_redirects=False):
        self.login()

        return self.get(self.find_url_from_route(redirect_to_route),
                        query_string=query_string,
                        follow_redirects=follow_redirects)

    def post_with_login(self, redirect_to_route, data):
        self.login()
        data['csrf_token'] = self.csrf_token

        return self.post(self.find_url_from_route(redirect_to_route), data=data, follow_redirects=True)
