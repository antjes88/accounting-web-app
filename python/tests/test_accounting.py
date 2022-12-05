# public libraries
import pytest
import pandas as pd

# own file
from tests.sql_statements import *


@pytest.mark.parametrize(
    "route, expected_response, expected_status_code",
    [
        ("accounting_menu", b'<!--accounting_menu this comment is to check that it is reached on test-->', 200),
        ("new_record", b'<!--accounting_new_record this comment is to check that it is reached on test-->', 200)
    ]
)
def test_accounting_pages_are_reached(client, route, expected_response, expected_status_code):
    """
    GIVEN a user surfing the web page
    WHEN tries to access accounting routes
    THEN makes sure that the right html is returned
    """
    response = client.get_with_login('accounting.' + route)

    assert expected_status_code == response.status_code
    assert expected_response in response.data


@pytest.fixture(scope='function')
def new_record_accounting_fixture_factory(db_conn):
    """
    Fixture that before and after the test truncate tables:
        - accounting.ledger_entries
        - accounting.transactions
        - accounting.accounts
    It also creates a dict with the values to be posted on route accounting.new_record.

    Args:
        db_conn: connector de database
    Returns: function _new_record_accounting_fixture_factory

    """
    db_conn.execute(TRUNCATE_TABLES)

    def _new_record_accounting_fixture_factory(debit, debit_account, credit, credit_account, amount, description, date):
        """
        Function that creates a dict with the values to be posted on route accounting.new_record to create a
        transaction.

        Args:
            debit: name of debit account type
            debit_account: name of debit account
            credit: name of credit account type
            credit_account: name of credit account
            amount: value of the transaction
            description: description of the transaction
            date: date of the transaction
        Returns: dict with the values to be posted on route accounting.new_record
        """
        data = {'account_type_debit': debit, 'account_type_credit': credit, 'amount': amount,
                'description': description, 'date': date,
                debit.lower() + '_account_debit': debit_account, credit.lower() + '_account_credit': credit_account}

        return data

    yield _new_record_accounting_fixture_factory

    db_conn.execute(TRUNCATE_TABLES)


@pytest.mark.parametrize(
    "debit, debit_father, debit_account, credit, credit_father, credit_account, amount, description, date",
    [
        ('Expense', 'Housing', 'Rent', 'Revenue', 'Salary', 'Basic Salary', 100.0, 'This is a test', '2021-01-01'),
        ('Revenue', 'Salary', 'Bonus', 'Expense', 'Leisure', 'Hotel', 400.0, 'This is a test', '1988-03-15'),
        ('Liability', 'Spain', 'Credit Line', 'Equity', 'Initial', 'Leisure', 400.0, 'This is a test', '2010-06-10'),
        ('Equity', 'Initial', 'Leisure', 'Liability', 'Spain', 'Credit Line',  400.0, 'This is a test', '2031-11-01'),
        ('Asset', 'Imaginary Account', 'LAccount', 'Expense', 'Leisure', 'Train Ticket', 100.0, 'Test', '2023-01-31'),
        ('Expense', 'Leisure', 'Train Ticket', 'Asset', 'Imaginary Account', 'LAccount', 500.0, 'Test', '1999-12-15'),
    ],
)
def test_accounting_insert_new_record(client, db_conn, new_record_accounting_fixture_factory,
                                      debit, debit_father, debit_account, credit,
                                      credit_father, credit_account, amount, description, date):
    """
    GIVEN a transaction to be recorded into the accounting database
    WHEN it is posted through the interface at route accounting.new_record
    THEN check that the correct records are created at destination database
    """
    data = new_record_accounting_fixture_factory(
        debit, debit_account, credit, credit_account, amount, description, date)
    db_conn.execute(
        INSERT_PROVIDED_ACCOUNTS % (debit, debit_father, credit, credit_father, debit_father, debit, debit_account,
                                    credit_father, credit, credit_account)
    )
    response = client.post_with_login('accounting.new_record', data.copy(), follow_redirects=True)

    results_at_db = db_conn.query(SELECT_FOR_ACCOUNTING_NEW_RECORD)

    expected_results = pd.DataFrame.from_dict({
        'transaction_date': [date] * 2,
        'transaction_description': [description] * 2,
        'amount': [amount] * 2,
        'entry_type_name': ['Credit', 'Debit'],
        'account_name': [credit_account, debit_account],
        'father_account_name': [credit_father, debit_father],
        'account_type_name': [credit, debit]
    })

    assert 200 == response.status_code
    assert b'<!--successful this comment is to check that it is reached on test-->' in response.data
    assert expected_results.equals(results_at_db)


@pytest.mark.parametrize(
    "debit, debit_account, credit, credit_account, amount, description, date, error_message",
    [
        ('Error', 'Line', 'Revenue', 'Bonus', 1.0, '', '2021-01-01', b'debit account type: Not a valid choice'),
        ('Liability', 'Line', 'Error', 'Bonus', 1.0, '', '2021-01-01', b'credit account type: Not a valid choice'),

        ('Liability', 'Error', 'Revenue', 'Bonus', 1.0, '', '2021-01-01', b'liability debit: Not a valid choice'),
        ('Asset', 'Error', 'Revenue', 'Bonus', 1.0, '', '2021-01-01', b'asset debit: Not a valid choice'),
        ('Equity', 'Error', 'Revenue', 'Bonus', 1.0, '', '2021-01-01', b'equity debit: Not a valid choice'),
        ('Expense', 'Error', 'Revenue', 'Bonus', 1.0, '', '2021-01-01', b'expense debit: Not a valid choice'),
        ('Revenue', 'Error', 'Revenue', 'Bonus', 1.0, '', '2021-01-01', b'revenue debit: Not a valid choice'),

        ('Revenue', 'Bonus', 'Liability', 'Error', 1.0, '', '2021-01-01', b'liability credit: Not a valid choice'),
        ('Revenue', 'Bonus', 'Asset', 'Error', 1.0, '', '2021-01-01', b'asset credit: Not a valid choice'),
        ('Revenue', 'Bonus', 'Equity', 'Error', 1.0, '', '2021-01-01', b'equity credit: Not a valid choice'),
        ('Revenue', 'Bonus', 'Expense', 'Error', 1.0, '', '2021-01-01', b'expense credit: Not a valid choice'),
        ('Revenue', 'Bonus', 'Revenue', 'Error', 1.0, '', '2021-01-01', b'revenue credit: Not a valid choice'),

        ('Revenue', 'Bonus', 'Liability', 'Line', None, '', '2021-01-01', b'amount: This field is required'),
        ('Revenue', 'Bonus', 'Liability', 'Line', None, '', None, b'date: This field is required'),
        ('Revenue', 'Bonus', 'Liability', 'Line', 'ed', '', '2021-01-01', b'amount: This field is required'),
        ('Revenue', 'Bonus', 'Liability', 'Line', 10.0, '', 'ed', b'date: This field is required'),
    ],
)
def test_accounting_new_records_field_value_not_valid(
        client, db_conn, new_record_accounting_fixture_factory, debit, debit_account, credit, credit_account, amount,
        description, date, error_message):
    """
    GIVEN a transaction to be recorded into the accounting database which does contain a not valid value
    WHEN it is posted through the interface at route accounting.new_record
    THEN check that the correct records are created at destination database
    """
    data = new_record_accounting_fixture_factory(
        debit, debit_account, credit, credit_account, amount, description, date)
    db_conn.execute(CREATE_DUMMY_ACCOUNTS)
    response = client.post_with_login('accounting.new_record', data.copy(), follow_redirects=True)

    with open('output.html', 'w') as file:
        file.write(str(response.data))

    assert error_message in response.data
