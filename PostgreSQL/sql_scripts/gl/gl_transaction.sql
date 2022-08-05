DROP TABLE IF EXISTS gl.transaction;

CREATE TABLE gl.transaction (
      transaction_id SERIAL PRIMARY KEY
    , account_id integer REFERENCES gl.account(account_id)
    , transaction_date DATE NOT NULL
    , transaction_accounting_date DATE NOT NULL
    , transaction_is_credit BOOLEAN NOT NULL
    , transaction_is_debit BOOLEAN NOT NULL
    , transaction_value NUMERIC(12,2) NOT NULL
    , transaction_comment VARCHAR(511)
);
