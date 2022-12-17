DROP TABLE IF EXISTS accounting.transactions CASCADE;

CREATE TABLE IF NOT EXISTS accounting.transactions (
      transaction_id SERIAL PRIMARY KEY
    , transaction_date DATE NOT NULL
    , transaction_description VARCHAR(255) NULL
    , created_by VARCHAR(50) NOT NULL DEFAULT 'SYSTEM'
    , created_date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);