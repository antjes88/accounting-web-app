# public libraries
import pandas as pd
from flask import render_template, request, url_for, redirect
from flask_login import login_required
import os
from postgresql_interface.postgresql_interface import postgres_sql_connector_factory

# own files
from . import accounting
from .forms import NewRecordForm
from .functions import *
from .sql_statements import *


@accounting.route('/accounting')
@login_required
def accounting_menu():
    """
    Landing route for accounting blueprint. It offers routes to create a new record or to delete current records.

    Returns: renders accounting/accounting_menu.html
    """
    return render_template('accounting/accounting_menu.html')


@accounting.route('/accounting/new_record', methods=['GET', 'POST'])
@login_required
def new_record():
    """
    Route to insert new records on accounting database.
    It creates a new transaction on accounting.transactions.
    It also creates a couple of entries on accounting.ledger_entries, a duple debit/credit.

    Returns:
          - If the operation is successful it creates the previously mentioned record on database and
            redirect to /successful
          - On failure it returns /error and provides an error message indicating the reason for the error.
    """
    try:
        db_conn = postgres_sql_connector_factory(
            vendor='GCP', host=os.environ['SERVER_HOST'], database_name=os.environ['DATABASE_NAME'],
            user_name=os.environ['USER_NAME'], user_password=os.environ['USER_PASSWORD'],
            port=os.environ['DATABASE_PORT_N'])
        accounts = db_conn.query(SELECT_ACCOUNTS_WITH_TYPES)

    except Exception as message:
        return redirect(url_for('home_page.error_page', message=message))

    form = NewRecordForm(accounts)

    if (form.validate_on_submit()) & (request.method == 'POST'):
        try:
            max_id = db_conn.query(SELECT_MAX_ID_TRANSACTIONS)['max_id'].values[0]
            new_transaction = pd.DataFrame.from_dict({
                'transaction_id': [str(max_id + 1)],
                'transaction_date': [form.date.data],
                'transaction_description': [str(form.description.data)]
            })
            db_conn.insert_table('accounting.transactions', new_transaction)

            if max_id == db_conn.query(SELECT_MAX_ID_TRANSACTIONS).values[0]:
                message = 'No record has being created on accounting.transactions table.'
                return redirect(url_for('home_page.error_page', message=message))
            else:
                credit_id, debit_id = get_entry_type_ids(db_conn)
                account_ids = db_conn.query(SELECT_ACCOUNT_IDS)
                account_debit_id = get_account_debit_id(account_ids, form)
                account_credit_id = get_account_credit_id(account_ids, form)
                new_ledger_entries = pd.DataFrame.from_dict({
                    'transaction_id': [str(max_id + 1), str(max_id + 1)],
                    'account_id': [str(account_debit_id), str(account_credit_id)],
                    'entry_type_id': [str(debit_id), str(credit_id)],
                    'amount': [str(form.amount.data), str(form.amount.data)],
                })
                db_conn.insert_table('accounting.ledger_entries', new_ledger_entries)

                if db_conn.query(SELECT_TRANSACTION_ID_IN_LEDGER_ENTRY % (max_id + 1)).shape[0] == 2:
                    return redirect(url_for('home_page.successful', blueprint='accounting', go_back_to='new_record'))
                else:
                    message = 'An error has occurred when populating data into accounting.ledger_entries table.'
                    return redirect(url_for('home_page.error_page', message=message))

        except Exception as message:
            return redirect(url_for('home_page.error_page', message=message))

    return render_template('accounting/new_record.html', form=form)
