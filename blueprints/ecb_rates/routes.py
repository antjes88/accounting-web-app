from flask import redirect, url_for
from flask_login import login_required

# own files
from . import ecb_rates
from .functions.ecbexchange import get_exchange_rates_from_ecb


@ecb_rates.route('/rates_ecb')
@login_required
def refresh_rates_ecb():
    message = get_exchange_rates_from_ecb()
    if message == 'Success':
        return redirect(url_for('home_page.successful', blueprint='home_page', go_back_to='home'))
    else:
        return redirect(url_for('home_page.error_page', message=message))
