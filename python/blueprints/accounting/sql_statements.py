SELECT_ACCOUNTS_WITH_TYPES = """
SELECT 
      INITCAP(at.account_type_name) AS account_type_name
    , acc.account_name
FROM accounting.accounts acc 
INNER JOIN accounting.account_types at
    ON at.account_type_id = acc.account_type_id
WHERE father_account_id IS NOT NULL
ORDER BY at.account_type_name, acc.account_name
"""

SELECT_MAX_ID_TRANSACTIONS = """
SELECT 
    CASE WHEN max(transaction_id) IS NULL THEN 0 ELSE max(transaction_id) END AS max_id 
FROM accounting.transactions
"""

SELECT_ENTRY_TYPE_IDS = """
SELECT 
      entry_type_id
    , UPPER(entry_type_name) AS entry_type_name 
FROM accounting.entry_types 
"""

SELECT_ACCOUNT_IDS = """
SELECT 
      account_id
    , UPPER(account_name) AS account_name 
FROM accounting.accounts;
"""

SELECT_TRANSACTION_ID_IN_LEDGER_ENTRY = """
SELECT 
      transaction_id
    , account_id
FROM accounting.ledger_entries
WHERE transaction_id = %s
"""