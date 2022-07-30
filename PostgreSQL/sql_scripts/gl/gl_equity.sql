DROP TABLE IF EXISTS gl.equity;

CREATE TABLE gl.equity (
      equity_id SERIAL PRIMARY KEY
    , currency_id INTEGER REFERENCES gl.currency(currency_id)
    , equity_type_id INTEGER REFERENCES gl.equity_type(equity_type_id)
    , equity_name VARCHAR(255) NOT NULL
    , equity_description VARCHAR(511) NOT NULL
    , equity_is_asset BOOLEAN NOT NULL
    , equity_is_liability BOOLEAN NOT NULL
);
