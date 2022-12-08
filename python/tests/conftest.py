# public libraries
import pytest
import os
from werkzeug.security import generate_password_hash
from postgresql_interface.postgresql_interface import postgres_sql_connector_factory

# own files
from main import app
from CommonResources.Classes.flask_csrf_test_client import *
from CommonResources.Classes.miscellaneous import Miscellaneous


CLIENT_PASSWORD_FOR_PYTEST_TEST = 'TEST-ENV'
CLIENT_USER_FOR_PYTEST_TEST = 'TEST-USER'
SECRET_KEY_PYTEST_TEST = 'QbWyySqspEKE9U8a4JppXpPhPAzuw6eG9ghyter'


@pytest.fixture(scope='function')
def overwrite_environment_variables():
    """
    Fixture that overwrite environment variables to execute pytest tests. Just in case that env files at local is
    set to connect to production, it changes it to connect to env/test database. This is relevant because some of the
    test requires to truncate tables in database

    Returns: change env variables for pytest tests purposes
    """
    Miscellaneous.env_var_loader('.test_env', file_path='tests')
    os.environ['PASSWORD'] = generate_password_hash(CLIENT_PASSWORD_FOR_PYTEST_TEST)
    os.environ['USER'] = CLIENT_USER_FOR_PYTEST_TEST
    os.environ['SECRET_KEY'] = SECRET_KEY_PYTEST_TEST


@pytest.fixture(scope='function')
def db_conn(overwrite_environment_variables):
    """
    Fixture that returns connector to database.

    Args:
        overwrite_environment_variables: fixture that overwrite environment variables
    Returns: API to interact with database in a sql manner.
    """
    return postgres_sql_connector_factory(
            vendor='GCP', host=os.environ['SERVER_HOST'], database_name=os.environ['DATABASE_NAME'],
            user_name=os.environ['USER_NAME'], user_password=os.environ['USER_PASSWORD'],
            port=os.environ['DATABASE_PORT_N'])


@pytest.fixture(scope='function')
def client(overwrite_environment_variables):
    """
    Fixture that sets the flask application for testing purposes.

    Args:
        overwrite_environment_variables: fixture that overwrite environment variables
    Returns: test client for the application build as CommonResources.Classes.flask_csrf_test_client.TestFlaskClient
    """
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = 'Test.localDomain'
    app.test_client_class = TestFlaskClient

    client = app.test_client()
    client.setup(CLIENT_PASSWORD_FOR_PYTEST_TEST, CLIENT_USER_FOR_PYTEST_TEST, 'login_page.login')

    return client


@pytest.fixture(scope='function')
def client_wrong_credentials():
    """
    Fixture that sets the flask application with wrong user credentials for testing purposes.

    Returns: test client for the application build as CommonResources.Classes.flask_csrf_test_client.TestFlaskClient
    """
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = 'Test.localDomain'
    app.test_client_class = TestFlaskClient

    client = app.test_client()
    client.setup(123456, 'wrong_user', 'login_page.login')

    return client
