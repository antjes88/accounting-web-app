# public libraries
import pytest
import os
from werkzeug.security import generate_password_hash
from postgresql_interface.postgresql_interface import PostgreSQL
import pandas as pd

# own files
from app import application
from CommonResources.Classes.flask_csrf_test_client import *
from tests.functions import check_on_accounting_new_insert_created
from tests.sql_statements import *


PASSWORD_FOR_TEST = 'TEST-ENV'
USER_FOR_TEST = 'TEST-USER'


@pytest.fixture(scope='session')
def db_conn():
    return PostgreSQL(os.environ['DATABASE_URL'])


@pytest.fixture(scope='function')
def client():
    os.environ['PASSWORD'] = generate_password_hash(PASSWORD_FOR_TEST)
    os.environ['USER'] = USER_FOR_TEST

    application.config['TESTING'] = True
    application.config['SERVER_NAME'] = 'Test.localDomain'
    application.test_client_class = FlaskClient

    client = application.test_client()
    client.setup(PASSWORD_FOR_TEST, USER_FOR_TEST, 'login_page.login')

    return client


@pytest.fixture(scope='function')
def client_wrong_credentials():
    application.config['TESTING'] = True
    application.config['SERVER_NAME'] = 'Test.localDomain'
    application.test_client_class = FlaskClient

    client = application.test_client()
    client.setup(123, 'wrong_user', 'login_page.login')

    return client


@pytest.fixture(scope='function')
def categories():
    json = [{"categoryid": 1, "categoryname": "House Expenses"},
            {"categoryid": 2, "categoryname": "Leisure"},
            {"categoryid": 3, "categoryname": "Petrol"}]
    category = pd.DataFrame(json)

    result_desired = [('None', 'Choose Category'),
                      ('House Expenses', 'House Expenses'),
                      ('Leisure', 'Leisure'),
                      ('Petrol', 'Petrol')]

    return category, result_desired


@pytest.fixture(scope='module')
def create_dummy_category(db_conn):
    category_name = 'PytestDummyCategory'
    db_conn.insert_table('accounting.category', pd.DataFrame({'categoryname': [category_name]}))

    yield category_name

    db_conn.execute("DELETE FROM accounting.category WHERE categoryname = '%s'" % category_name)


@pytest.fixture(scope='module')
def new_record_accounting_fixture_factory(create_dummy_category, db_conn):
    created_records = []

    def _new_record_accounting_fixture_factory(table, value, to_balance, category, description, date):
        record = {'table': table, 'value': value, 'to_balance': to_balance, 'category': category,
                  'description': description, 'date': date}
        if record['category'] == '':
            record['category'] = create_dummy_category
        created_records.append(record)

        return record

    yield _new_record_accounting_fixture_factory

    for recorded in created_records:
        result, id_to_delete = check_on_accounting_new_insert_created(recorded, return_id=True)
        if result:
            db_conn.execute("DELETE FROM %s WHERE id = %s" % (recorded['table'], id_to_delete))


@pytest.fixture()
def data_to_create_category(db_conn):
    new_category = 'PytestCreateCategory'

    yield {'category': 'None', 'new_category': new_category, 'to_delete': '0'}

    db_conn.execute("DELETE FROM accounting.category WHERE categoryname = '%s'" % new_category)


@pytest.fixture()
def create_dummy_category_to_be_deleted(db_conn):
    category_name = 'PytestForDelete'
    db_conn.insert_table('accounting.category', pd.DataFrame({'categoryname': [category_name]}))

    return {'category': category_name, 'new_category': 'None', 'to_delete': '1'}


@pytest.fixture()
def loading_env_var():
    file_name = '.testingenv'
    file_path = os.path.join(os.getcwd(), file_name)

    env_var_value = '1234'
    env_var_name = 'TEST'
    file_content = '%s=%s' % (env_var_name, env_var_value)

    with open(file_path, "w") as f:
        f.write(file_content)

    yield file_name, env_var_value, env_var_name

    os.remove(file_path)


@pytest.fixture()
def df_to_html():
    data = {'Id': [1, 2, 3, 4, 5],
            'Model': ['Focus', 'Fiesta', 'Corsa', 'Insignia', 'Vectra'],
            'Year': [2012, 2020, 2017, 2019, 2014]}
    df = pd.DataFrame.from_dict(data)

    return df


@pytest.fixture()
def dataframes():
    data_to_test = {'Id': [1, 2, 3],
                    'Currency': [100, 200, 300]}
    df_to_test = pd.DataFrame.from_dict(data_to_test)
    data_to_compare = {'Id': [1, 2, 3],
                       'Currency': ['£ 100.00', '£ 200.00', '£ 300.00']}
    df_to_compare = pd.DataFrame.from_dict(data_to_compare)
    return df_to_test, df_to_compare


@pytest.fixture(scope='module')
def create_dummy_category_return_id(db_conn):
    category_name = 'PytestReturnId'
    db_conn.insert_table('accounting.category', pd.DataFrame({'categoryname': [category_name]}))
    category_id = db_conn.query(
        "SELECT categoryid FROM accounting.category WHERE categoryname = '%s'" % category_name)['categoryid'].values[0]

    yield category_id

    db_conn.execute("DELETE FROM accounting.category WHERE categoryname = '%s'" % category_name)


@pytest.fixture(scope='module')
def created_value_to_be_deleted_fixture_factory(create_dummy_category_return_id, db_conn):
    created_records = []

    def _created_value_to_be_deleted_fixture_factory(table, value, to_balance, description, date):
        to_insert = pd.DataFrame({'value': [value], 'categoryid': [create_dummy_category_return_id],
                                  'description': [description], 'date': [date], 'tobalance': to_balance})

        if table == 'accounting.SpainExpenses':
            db_conn.insert_table(table, to_insert[['value', 'date', 'description']])
            id_to_delete = db_conn.query(
                SELECT_MAX_ID_ACCOUNTING_EXPENSES_SPAIN_EXPENSES % (
                    table, description, value, date)
            )['id'].values[0]

        elif table == 'accounting.AccountingAdjustments':
            db_conn.insert_table(table, to_insert[['value', 'categoryid', 'date', 'description', 'tobalance']])
            id_to_delete = db_conn.query(
                SELECT_MAX_ID_ACCOUNTING_EXPENSES_ADJUSTMENTS % (
                    table, description, value, create_dummy_category_return_id, date, to_balance)
            )['id'].values[0]

        else:
            db_conn.insert_table(table, to_insert[['value', 'categoryid', 'date', 'description']])
            id_to_delete = db_conn.query(
                SELECT_MAX_ID_ACCOUNTING_EXPENSES_INCOMES % (
                    table, description, value, create_dummy_category_return_id, date)
            )['id'].values[0]

        created_records.append({table: id_to_delete})

        return id_to_delete

    yield _created_value_to_be_deleted_fixture_factory

    # this is just to make sure that rows created are truly deleted
    for recorded in created_records:
        for rec in recorded:
            db_conn.execute("DELETE FROM %s WHERE id = %s" % (rec, recorded[rec]))


@pytest.fixture(scope='function')
def xml_test_file_content():
    with open(os.path.join(os.getcwd(),'tests/data/xml_ecb_test.xml')) as f:
        response = f.read()

    return response


@pytest.fixture(scope='function')
def result_expected_xml_test_file_content():
    data = {"Fecha": {"0": "2021-05-26", "1": "2021-05-27", "2": "2021-05-28"},
            "Libra": {"0": 0.8633, "1": 0.86068, "2": 0.85765},
            "Dolar": {"0": 1.2229, "1": 1.2198, "2": 1.2142},
            "Createdby": {"0": "System", "1": "System", "2": "System"},
            }
    result = pd.DataFrame(data)
    result.columns.name = None

    return result


@pytest.fixture(scope='function')
def change_temporally_ecb_database(db_conn):
    # there is no ecb_db test instance, so it is done on the cuentas_db test instance
    ecb_db_credentials = os.environ['HEROKU_POSTGRESQL_PUCE_URL']
    test_db_credential = os.environ['DATABASE_URL']
    os.environ['HEROKU_POSTGRESQL_PUCE_URL'] = test_db_credential

    db_conn.execute(CREATE_ECB_RATES_TABLE)

    yield

    os.environ['HEROKU_POSTGRESQL_PUCE_URL'] = ecb_db_credentials
    db_conn.execute(DROP_ECB_RATES_TABLE)


@pytest.fixture(scope='module')
def created_dummy_product_assets(db_conn):
    dummy_name = 'Pytest'
    ids = {}
    for table in ['company', 'division', 'category', 'subcategory', 'currency']:
        db_conn.insert_table('assets.%s' % table, pd.DataFrame({table: [dummy_name + table]}))
        ids[table] = db_conn.query("SELECT %sid FROM assets.%s WHERE %s = '%s'" % (
            table, table, table, dummy_name + table))[table + 'id'].values[0]

    product_test_name = 'pytest test product'
    product = pd.DataFrame({'CompanyId': [ids['company']],
                            'DivisionId': [ids['division']],
                            'CategoryId': [ids['category']],
                            'SubCategoryId': [ids['subcategory']],
                            'CurrencyId': [ids['currency']],
                            'Product': [product_test_name],
                            'PensionPlan': [False],
                            'FixedYield': [False]})
    db_conn.insert_table('assets.product', product)
    product_id = db_conn.query(
        "SELECT productid FROM assets.product WHERE product = '%s'" % product_test_name)['productid'].values[0]

    yield product_test_name, product_id

    db_conn.execute("DELETE FROM assets.value WHERE productid = %s" % product_id)
    db_conn.execute("DELETE FROM assets.product WHERE productid = %s" % product_id)
    for key in ids:
        db_conn.execute("DELETE FROM assets.%s WHERE %sid = %s" % (key, key, ids[key]))
