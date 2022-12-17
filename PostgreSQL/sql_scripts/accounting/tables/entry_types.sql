DROP TABLE IF EXISTS accounting.entry_types CASCADE;

CREATE TABLE IF NOT EXISTS accounting.entry_types (
      entry_type_id SERIAL PRIMARY KEY
    , entry_type_name VARCHAR(50) NOT NULL UNIQUE
    , created_by VARCHAR(50) NOT NULL DEFAULT 'SYSTEM'
    , created_date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO accounting.entry_types
(entry_type_name)
VALUES
('Credit'),
('Debit');