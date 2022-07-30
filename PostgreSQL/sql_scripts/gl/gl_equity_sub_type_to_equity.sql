DROP TABLE IF EXISTS gl.equity_sub_type_to_equity;

CREATE TABLE gl.equity_sub_type_to_equity (
      equity_sub_type_to_equity_id SERIAL PRIMARY KEY
    , equity_id INTEGER REFERENCES gl.equity(equity_id)
    , equity_sub_type_id INTEGER REFERENCES gl.equity_sub_type(equity_sub_type_id)
);
