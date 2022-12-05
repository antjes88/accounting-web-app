DROP TABLE IF EXISTS accounting.ledger_entries CASCADE;

CREATE TABLE IF NOT EXISTS accounting.ledger_entries (
      transaction_id INT REFERENCES accounting.transactions(transaction_id) NOT NULL
    , account_id INT REFERENCES accounting.accounts(account_id) NOT NULL
    , entry_type_id INT REFERENCES accounting.entry_types(entry_type_id) NOT NULL
    , amount NUMERIC(10, 2) NOT NULL
    , PRIMARY KEY (transaction_id, account_id)
);