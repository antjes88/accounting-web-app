DROP TABLE IF EXISTS gl.equity_sub_type;

CREATE TABLE gl.equity_sub_type (
      equity_type_sub_id SERIAL PRIMARY KEY
    , equity_type_id INTEGER REFERENCES gl.equity_type(equity_type_id)
    , equity_sub_type_name VARCHAR(100) NOT NULL
);