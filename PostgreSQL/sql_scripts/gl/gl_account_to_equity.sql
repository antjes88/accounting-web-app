DROP TABLE IF EXISTS gl.account_to_equity;

CREATE TABLE gl.account_to_equity (
      account_to_equity_id SERIAL PRIMARY KEY
    , account_id INTEGER REFERENCES gl.account(account_id)
    , equity_id INTEGER REFERENCES gl.equity(equity_id)
    , account_to_equity_share NUMERIC(8,6) NOT NULL
    , account_to_equity_from_date DATE NOT NULL
    , account_to_equity_to_date DATE
    , account_to_equity_current BOOLEAN NOT NULL
);
