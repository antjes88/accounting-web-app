# generic libraries
from flask import redirect, url_for
from flask_login import login_required

# own files
from . import ecb_rates
from .functions.ecb_exchange_rates import call_to_ecb_api_exchange_rate, from_xml_to_dataframe, \
    load_to_database_eur_exchange_rate


DAYS_TO_REGISTER = 10  # this is out here for testing purposes


@ecb_rates.route('/rates_ecb')
@login_required
def refresh_rates_ecb():
    """
    Get exchange rates from European Central Bank (ECB) for the last 10 days.

    Returns:
        - If operation is successful returns "home_page.successful" to client and loads last 10 days of EUR exchange
          rates to ecb.eur_exchange_rate
        - On failure it returns "home_page.error_page" reporting the error encountered.
    """
    try:
        response = call_to_ecb_api_exchange_rate(DAYS_TO_REGISTER)
        exchange_df = from_xml_to_dataframe(response.text)
        load_to_database_eur_exchange_rate(exchange_df)

        return redirect(url_for('home_page.successful', blueprint='home_page', go_back_to='home'))
    except Exception as e:
        return redirect(url_for('home_page.error_page', message=e))
