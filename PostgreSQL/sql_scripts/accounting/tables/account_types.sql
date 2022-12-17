DROP TABLE IF EXISTS accounting.account_types CASCADE;

CREATE TABLE IF NOT EXISTS accounting.account_types (
      account_type_id SERIAL PRIMARY KEY
    , account_type_name VARCHAR(50) NOT NULL UNIQUE
    , created_by VARCHAR(50) NOT NULL DEFAULT 'SYSTEM'
    , created_date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO accounting.account_types
(account_type_name)
VALUES
('Asset'),
('Liability'),
('Equity'),
('Revenue'),
('Expense');