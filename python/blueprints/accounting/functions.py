from .sql_statements import *


def get_account_debit_id(account_ids, form):
    """
    Function that returns the account id for the debit side of the transaction. In order to do it, it checks the account
    type to access the right attribute of form.

    Args:
        account_ids: pandas dataframe from SELECT_ACCOUNT_IDS
        form: instance of class NewRecordForm
    Returns: id of the debit account in agreement to flask session
    """
    if form.account_type_debit.data == 'Asset':
        return account_ids[account_ids['account_name'] == form.asset_account_debit.data.upper()]['account_id'].values[0]
    elif form.account_type_debit.data == 'Equity':
        return account_ids[
            account_ids['account_name'] == form.equity_account_debit.data.upper()]['account_id'].values[0]
    elif form.account_type_debit.data == 'Expense':
        return account_ids[
            account_ids['account_name'] == form.expense_account_debit.data.upper()]['account_id'].values[0]
    elif form.account_type_debit.data == 'Liability':
        return account_ids[
            account_ids['account_name'] == form.liability_account_debit.data.upper()]['account_id'].values[0]
    elif form.account_type_debit.data == 'Revenue':
        return account_ids[
            account_ids['account_name'] == form.revenue_account_debit.data.upper()]['account_id'].values[0]
    else:
        return None


def get_account_credit_id(account_ids, form):
    """
    Function that returns the account id for the credit side of the transaction. In order to do it, it checks the
    account type to access the right attribute of form.

    Args:
        account_ids: pandas dataframe from SELECT_ACCOUNT_IDS
        form: instance of class NewRecordForm
    Returns: id of the credit account in agreement to flask session
    """
    if form.account_type_credit.data == 'Asset':
        return account_ids[
            account_ids['account_name'] == form.asset_account_credit.data.upper()]['account_id'].values[0]
    elif form.account_type_credit.data == 'Equity':
        return account_ids[
            account_ids['account_name'] == form.equity_account_credit.data.upper()]['account_id'].values[0]
    elif form.account_type_credit.data == 'Expense':
        return account_ids[
            account_ids['account_name'] == form.expense_account_credit.data.upper()]['account_id'].values[0]
    elif form.account_type_credit.data == 'Liability':
        return account_ids[
            account_ids['account_name'] == form.liability_account_credit.data.upper()]['account_id'].values[0]
    elif form.account_type_credit.data == 'Revenue':
        return account_ids[
            account_ids['account_name'] == form.revenue_account_credit.data.upper()]['account_id'].values[0]
    else:
        return None


def get_entry_type_ids(db_conn):
    """
    Function that returns entry_type_id for Credit and Debit. These ids are taken from accounting.entry_types.

    Args:
        db_conn: connector to database
    Returns: id for credit and debit.
    """
    entry_type_ids = db_conn.query(SELECT_ENTRY_TYPE_IDS)
    credit_id = entry_type_ids[entry_type_ids['entry_type_name'] == 'CREDIT']['entry_type_id'].values[0]
    debit_id = entry_type_ids[entry_type_ids['entry_type_name'] == 'DEBIT']['entry_type_id'].values[0]

    return credit_id, debit_id
