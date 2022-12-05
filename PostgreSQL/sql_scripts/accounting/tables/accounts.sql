DROP TABLE IF EXISTS accounting.accounts CASCADE;

CREATE TABLE IF NOT EXISTS accounting.accounts (
      account_id SERIAL PRIMARY KEY
    , father_account_id INT REFERENCES accounting.accounts(account_id) NULL
    , account_type_id INT REFERENCES accounting.account_types(account_type_id) NOT NULL
    , account_name VARCHAR(100) NOT NULL UNIQUE
    , is_physical BOOLEAN NOT NULL DEFAULT TRUE
    , is_archived BOOLEAN NOT NULL DEFAULT FALSE
);
