# public libraries
import pytest
import os

# own files
from tests.sql_statements import *


@pytest.fixture(scope="function")
def pgadmin_tables(db_conn):
    return db_conn.query(SELECT_PGADMIN_TABLES)


@pytest.mark.parametrize(
    "table_schema, table_name",
    [
        ("accounting", "account_types"),
        ("accounting", "accounts"),
        ("accounting", "entry_types"),
        ("accounting", "ledger_entries"),
        ("accounting", "transactions")
     ]
)
def test_tables_exists_at_destination_database(pgadmin_tables, table_schema, table_name):
    """
    GIVEN the tables needed for the accounting database
    WHEN it is compared with the tables at destination database
    THEN all should be found
    """
    assert pgadmin_tables[
        (pgadmin_tables['table_schema'] == table_schema.upper())
        & (pgadmin_tables['table_name'] == table_name.upper())
           ].shape[0] == 1


@pytest.fixture(scope="function")
def pgadmin_sequences(db_conn):
    return db_conn.query(SELECT_INFORMATION_SCHEMA_SEQUENCES)


@pytest.mark.parametrize(
    "sequence_schema, sequence_name",
    [
        ("accounting", "account_types_account_type_id_seq"),
        ("accounting", "accounts_account_id_seq"),
        ("accounting", "entry_types_entry_type_id_seq"),
        ("accounting", "transactions_transaction_id_seq")
     ]
)
def test_sequences_exists_at_destination_database(pgadmin_sequences, sequence_schema, sequence_name):
    """
    GIVEN the sequences needed for the accounting database
    WHEN it is compared with the sequences at destination database
    THEN check that they exists
    """
    assert pgadmin_sequences[
        (pgadmin_sequences['sequence_schema'] == sequence_schema.upper())
        & (pgadmin_sequences['sequence_name'] == sequence_name.upper())
           ].shape[0] == 1


@pytest.fixture(scope="function")
def pgadmin_privileges(db_conn):
    return db_conn.query(SELECT_PGADMIN_PRIVILEGES % (os.environ['USER_NAME'], os.environ['DATABASE_NAME']))


@pytest.mark.parametrize(
    "table_schema, table_name",
    [
        ("accounting", "account_types"),
        ("accounting", "accounts"),
        ("accounting", "entry_types"),
        ("accounting", "ledger_entries"),
        ("accounting", "transactions")
     ]
)
def test_user_permissions_for_tables_exists_at_destination_database(pgadmin_privileges, table_schema, table_name):
    """
    GIVEN the tables needed for the accounting database
    WHEN it is compared with the tables at destination database
    THEN check that the user has been granted the needed permissions
    """
    assert pgadmin_privileges[
        (pgadmin_privileges['table_schema'] == table_schema.upper())
        & (pgadmin_privileges['table_name'] == table_name.upper())
           ]['privilege'].values[0] == 'DELETE, INSERT, REFERENCES, SELECT, TRIGGER, TRUNCATE, UPDATE'


def test_values_preload_values_for_entry_types(db_conn):
    """
    GIVEN the accounting.entry_types that should be created and populated
    WHEN it is load to the destination database
    THEN check that those values have been created
    """
    entry_types_names = db_conn.query(SELECT_ENTRY_TYPE_NAMES)
    assert entry_types_names['entry_type_name'].tolist() == ['CREDIT', 'DEBIT']


def test_values_preload_values_for_account_types(db_conn):
    """
    GIVEN the accounting.account_types that should be created and populated
    WHEN it is load to the destination database
    THEN check that those values have been created
    """
    account_types_names = db_conn.query(SELECT_ACCOUNT_TYPE_NAMES)
    assert account_types_names['account_type_name'].tolist() == ['ASSET', 'EQUITY', 'EXPENSE', 'LIABILITY', 'REVENUE']
