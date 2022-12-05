DROP TABLE IF EXISTS accounting.transactions CASCADE;

CREATE TABLE IF NOT EXISTS accounting.transactions (
      transaction_id SERIAL PRIMARY KEY
    , transaction_date DATE NOT NULL
    , transaction_description VARCHAR(255) NULL
);