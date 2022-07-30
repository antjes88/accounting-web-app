from blueprints.ecb_rates.functions.ecbexchange import from_xml_to_dataframe, DAYS_TO_REGISTER
import datetime as dt


def test_from_xml_to_dataframe(xml_test_file_content, result_expected_xml_test_file_content):
    exchange_rates = from_xml_to_dataframe(xml_test_file_content)

    # this column is created with the datetime of the moment so can not be compare
    exchange_rates.drop(columns=['Created'], inplace=True)

    comparison = exchange_rates.sort_index().sort_index(
        axis=1).values == result_expected_xml_test_file_content.sort_index().sort_index(axis=1).values
    assert comparison.all().all()


def test_refresh_rates_ecb(change_temporally_ecb_database, client, db_conn):
    response = client.get_with_login('ecb_rates.refresh_rates_ecb', follow_redirects=True)

    # # this is to get how many weekdays are in the interval extracted. This is due to the fact that the ECB API only
    # # provides rates for weekdays
    # total_week_days = 0
    # for x in range(0, DAYS_TO_REGISTER + 1):
    #     if (dt.datetime.date(dt.datetime.now()) - dt.timedelta(x)).isoweekday() not in [6, 7]:
    #         total_week_days += 1

    days_inserted = db_conn.query("SELECT COUNT(*) FROM bce.EuroaRatio").values[0]

    assert 200 == response.status_code
    assert b'<!--successful this comment is to check that it is reached on test-->' in response.data
    assert days_inserted > 0
