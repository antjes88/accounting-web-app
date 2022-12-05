TRUNCATE_TABLES = """
TRUNCATE TABLE accounting.ledger_entries CASCADE;
TRUNCATE TABLE accounting.transactions CASCADE;
TRUNCATE TABLE accounting.accounts CASCADE;
"""

SELECT_PGADMIN_TABLES = """
SELECT 
    UPPER(schemaname) AS table_schema,  
    UPPER(tablename) AS table_name
FROM pg_catalog.pg_tables
WHERE schemaname != 'pg_catalog' AND 
    schemaname != 'information_schema';
"""

SELECT_PGADMIN_PRIVILEGES = """
SELECT 
      UPPER(table_schema) AS table_schema
    , UPPER(table_name) AS table_name
    , ARRAY_TO_STRING(ARRAY_AGG(UPPER(privilege_type) ORDER BY privilege_type), ', ') AS privilege
FROM information_schema.table_privileges 
WHERE table_schema != 'pg_catalog' 
    AND table_schema != 'information_schema' 
    AND grantee = '%s'
    AND table_catalog = '%s'
GROUP BY table_schema, table_name;
"""

SELECT_ENTRY_TYPE_NAMES = """
SELECT 
      entry_type_id
    , UPPER(entry_type_name) AS entry_type_name 
FROM accounting.entry_types 
ORDER BY entry_type_name
"""

SELECT_ACCOUNT_TYPE_NAMES = """
SELECT 
      account_type_id
    , UPPER(account_type_name) AS account_type_name 
FROM accounting.account_types 
ORDER BY account_type_name
"""

SELECT_INFORMATION_SCHEMA_SEQUENCES = """
SELECT 
      UPPER(sequence_schema) AS sequence_schema
    , UPPER(sequence_name) AS sequence_name
FROM information_schema.sequences 
ORDER BY sequence_name 
"""

CREATE_DUMMY_ACCOUNTS = """
INSERT INTO accounting.accounts
(father_account_id, account_type_id, account_name)
VALUES
(NULL, (SELECT account_type_id FROM accounting.account_types WHERE UPPER(account_type_name) = 'REVENUE'), 'Salary'),
(NULL, (SELECT account_type_id FROM accounting.account_types WHERE UPPER(account_type_name) = 'EXPENSE'), 'Housing'),
(NULL, (SELECT account_type_id FROM accounting.account_types WHERE UPPER(account_type_name) = 'ASSET'), 'Imaginary Bank Account'),
(NULL, (SELECT account_type_id FROM accounting.account_types WHERE UPPER(account_type_name) = 'EQUITY'), 'Initial Balances'),
(NULL, (SELECT account_type_id FROM accounting.account_types WHERE UPPER(account_type_name) = 'LIABILITY'), 'Spain');

INSERT INTO accounting.accounts
(father_account_id, account_type_id, account_name)
VALUES
((SELECT account_id FROM accounting.accounts WHERE UPPER(account_name) = 'SALARY'), (SELECT account_type_id FROM accounting.account_types WHERE UPPER(account_type_name) = 'REVENUE'), 'Basic Salary'),
((SELECT account_id FROM accounting.accounts WHERE UPPER(account_name) = 'SALARY'), (SELECT account_type_id FROM accounting.account_types WHERE UPPER(account_type_name) = 'REVENUE'), 'Bonus'),
((SELECT account_id FROM accounting.accounts WHERE UPPER(account_name) = 'HOUSING'), (SELECT account_type_id FROM accounting.account_types WHERE UPPER(account_type_name) = 'EXPENSE'), 'Rent'),
((SELECT account_id FROM accounting.accounts WHERE UPPER(account_name) = 'HOUSING'), (SELECT account_type_id FROM accounting.account_types WHERE UPPER(account_type_name) = 'EXPENSE'), 'Home Appliances'),
((SELECT account_id FROM accounting.accounts WHERE UPPER(account_name) = 'IMAGINARY BANK ACCOUNT'), (SELECT account_type_id FROM accounting.account_types WHERE UPPER(account_type_name) = 'ASSET'), 'Usual Expenses Account'),
((SELECT account_id FROM accounting.accounts WHERE UPPER(account_name) = 'INITIAL BALANCES'), (SELECT account_type_id FROM accounting.account_types WHERE UPPER(account_type_name) = 'EQUITY'), 'Initial Imaginary Balances'),
((SELECT account_id FROM accounting.accounts WHERE UPPER(account_name) = 'SPAIN'), (SELECT account_type_id FROM accounting.account_types WHERE UPPER(account_type_name) = 'LIABILITY'), 'Line');
"""

SELECT_ACCOUNTS = """
SELECT 
      at.account_type_name
    , acc.account_name 
FROM accounting.accounts acc
INNER JOIN accounting.account_types at
    ON at.account_type_id = acc.account_type_id
WHERE acc.father_account_id IS NOT NULL;
"""

INSERT_PROVIDED_ACCOUNTS = """
INSERT INTO accounting.accounts
(father_account_id, account_type_id, account_name)
VALUES
(NULL, (SELECT account_type_id FROM accounting.account_types WHERE UPPER(account_type_name) = UPPER('%s')), '%s'),
(NULL, (SELECT account_type_id FROM accounting.account_types WHERE UPPER(account_type_name) = UPPER('%s')), '%s');

INSERT INTO accounting.accounts
(father_account_id, account_type_id, account_name)
VALUES
((SELECT account_id FROM accounting.accounts WHERE UPPER(account_name) = UPPER('%s')), (SELECT account_type_id FROM accounting.account_types WHERE UPPER(account_type_name) = UPPER('%s')), '%s'),
((SELECT account_id FROM accounting.accounts WHERE UPPER(account_name) = UPPER('%s')), (SELECT account_type_id FROM accounting.account_types WHERE UPPER(account_type_name) = UPPER('%s')), '%s');
"""

SELECT_FOR_ACCOUNTING_NEW_RECORD = """
SELECT
      TO_CHAR(TR.transaction_date, 'YYYY-MM-DD') AS transaction_date
    , TR.transaction_description
    , LE.amount
    , ET.entry_type_name
    , ACC1.account_name
    , ACC2.account_name AS father_account_name
    , AT.account_type_name
FROM accounting.ledger_entries LE
INNER JOIN accounting.transactions TR
    ON LE.transaction_id = TR.transaction_id
INNER JOIN accounting.entry_types ET
    ON LE.entry_type_id = ET.entry_type_id
INNER JOIN accounting.accounts ACC1
    ON LE.account_id = ACC1.account_id
INNER JOIN accounting.account_types AT
    ON AT.account_type_id = ACC1.account_type_id
LEFT JOIN accounting.accounts ACC2
    ON ACC1.father_account_id = ACC2.account_id
ORDER BY ET.entry_type_name;
"""