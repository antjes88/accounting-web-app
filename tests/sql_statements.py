SELECT_ACCOUNTING_NEW_INSERT_SPAIN = """
SELECT 
    id, 
    cast(date as varchar) as date, 
    value, 
    description  
FROM %s 
WHERE ID IN (SELECT MAX(ID) FROM %s)
"""

SELECT_ACCOUNTING_NEW_INSERT_INCOMES_OR_EXPENSES = """
SELECT 
    tab.id, 
    cat.categoryname as category, 
    cast(tab.date as varchar) as date, 
    tab.value, 
    tab.description
FROM %s tab 
INNER JOIN accounting.category cat 
    ON cat.categoryid = tab.categoryid 
WHERE ID IN (SELECT MAX(ID) FROM %s)
"""

SELECT_ACCOUNTING_NEW_INSERT_ADJUSTMENTS = """
SELECT 
    tab.id, 
    cat.categoryname as category, 
    cast(tab.date as varchar) as date, 
    tab.value, 
    tab.description,
    CASE WHEN tab.tobalance is true THEN '1' ELSE '0' END as to_balance
FROM %s tab 
INNER JOIN accounting.category cat 
    ON cat.categoryid = tab.categoryid 
WHERE ID IN (SELECT MAX(ID) FROM %s)
"""

SELECT_MAX_ID_ACCOUNTING_EXPENSES_INCOMES = """
SELECT id 
FROM %s 
WHERE description = '%s' 
    AND value = %s 
    AND categoryid = %s
    AND date = '%s'
"""

SELECT_MAX_ID_ACCOUNTING_EXPENSES_SPAIN_EXPENSES = """
SELECT id 
FROM %s 
WHERE description = '%s' 
    AND value = %s 
    AND date = '%s'
"""

SELECT_MAX_ID_ACCOUNTING_EXPENSES_ADJUSTMENTS = """
SELECT id 
FROM %s 
WHERE description = '%s' 
    AND value = %s 
    AND categoryid = %s
    AND date = '%s'
    AND tobalance = %s
"""

CREATE_ECB_RATES_TABLE = """
CREATE SCHEMA bce

CREATE TABLE bce.EuroaRatio
(
Fecha DATE PRIMARY KEY,
Libra NUMERIC(10,4) NOT NULL,
Dolar NUMERIC(10,4) NOT NULL,
Created Date NOT NULL,
CreatedBy varchar(100) Not NUll
)
"""

DROP_ECB_RATES_TABLE = """
TRUNCATE TABLE bce.EuroaRatio;

DROP TABLE bce.EuroaRatio;

DROP SCHEMA bce
"""
