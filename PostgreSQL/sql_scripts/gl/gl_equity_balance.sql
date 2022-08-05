DROP TABLE IF EXISTS gl.equity_balance;

CREATE TABLE gl.equity_balance (
      equity_balance_id SERIAL PRIMARY KEY
    , equity_id INTEGER REFERENCES gl.equity(equity_id)
    , platform_id INTEGER REFERENCES gl.account(account_id)
    , equity_balance_date DATE NOT NULL
    , equity_balance_value NUMERIC(10,2) NOT NULL
);
