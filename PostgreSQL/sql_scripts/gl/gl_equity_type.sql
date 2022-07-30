DROP TABLE IF EXISTS gl.equity_type;

CREATE TABLE gl.equity_type (
      equity_type_id SERIAL PRIMARY KEY
    , equity_family_type_id INTEGER REFERENCES gl.equity_family_type(equity_family_type_id)
    , equity_type_name VARCHAR(100) NOT NULL
);