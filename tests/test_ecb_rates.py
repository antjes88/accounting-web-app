from blueprints.ecb_rates.functions.ecb_exchange_rates import from_xml_to_dataframe, call_to_ecb_api_exchange_rate
from blueprints.ecb_rates.routes import DAYS_TO_REGISTER
import pytest
import os
import pandas as pd
import datetime as dt


def test_from_xml_to_dataframe():
    """
    GIVEN an answer from ECB API
    WHEN it is processed by function from_xml_to_dataframe()
    THEN it should be the equal to result_expected_from_xml
    """
    with open(os.path.join(os.getcwd(), 'tests/data/xml_ecb_test.xml')) as f:
        exchange_rates = from_xml_to_dataframe(f.read())

    # this column is created with the datetime of the moment so cannot be compared
    exchange_rates.drop(columns=['eur_exchange_rate_created_date'], inplace=True)

    data = {
        "eur_exchange_rate_date": ["2021-05-26", "2021-05-27", "2021-05-28"],
        "eur_exchange_rate_to_gbp": [0.8633, 0.86068, 0.85765],
        "eur_exchange_rate_to_dollar": [1.2229, 1.2198, 1.2142],
        "eur_exchange_rate_created_by": ["System", "System", "System"],
    }
    result_expected_from_xml = pd.DataFrame(data)

    assert exchange_rates.equals(result_expected_from_xml)


@pytest.fixture(scope='function')
def truncate_ecb__eur_exchange_rate(db_conn):
    """
    Fixture that ensures that ecb.eur_exchange_rate is truncated before and after the test.

    Args:
        db_conn: call to fixture that creates connector to db
    """
    db_conn.execute("TRUNCATE TABLE ecb.eur_exchange_rate")
    yield
    db_conn.execute("TRUNCATE TABLE ecb.eur_exchange_rate")


def test_refresh_rates_ecb(truncate_ecb__eur_exchange_rate, client, db_conn):
    """
    GIVEN a call to route ecb_rates/rates_ecb
    WHEN the result is successful
    THEN check that the values are correctly uploaded to ecb.eur_exchange_rate
    """
    cols = ['eur_exchange_rate_date', 'eur_exchange_rate_created_by', 'eur_exchange_rate_to_gbp',
            'eur_exchange_rate_to_dollar']
    response = call_to_ecb_api_exchange_rate(DAYS_TO_REGISTER)
    exchange_df = from_xml_to_dataframe(response.text)

    response_from_route = client.get_with_login('ecb_rates.refresh_rates_ecb', follow_redirects=True)
    exchange_at_db = db_conn.query("SELECT * FROM ecb.eur_exchange_rate")

    for col in ['eur_exchange_rate_to_dollar', 'eur_exchange_rate_to_gbp']:
        exchange_df[col] = exchange_df[col].apply(lambda x: round(x, 4))
    exchange_at_db['eur_exchange_rate_date'] = exchange_at_db['eur_exchange_rate_date'].apply(
        lambda x: dt.datetime.strftime(x, '%Y-%m-%d'))

    assert 200 == response_from_route.status_code
    assert b'<!--successful this comment is to check that it is reached on test-->' in response_from_route.data
    assert exchange_at_db[cols].equals(exchange_df[cols])  # this could not be true if the execution is done at midnight
