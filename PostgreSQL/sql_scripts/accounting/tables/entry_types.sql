DROP TABLE IF EXISTS accounting.entry_types CASCADE;

CREATE TABLE IF NOT EXISTS accounting.entry_types (
      entry_type_id SERIAL PRIMARY KEY
    , entry_type_name VARCHAR(50) NOT NULL UNIQUE
);

INSERT INTO accounting.entry_types
(entry_type_name)
VALUES
('Credit'),
('Debit');