DROP TABLE IF EXISTS gl.sector_composition;

CREATE TABLE gl.sector_composition (
      sector_composition_id SERIAL PRIMARY KEY
    , sector_id INTEGER REFERENCES gl.account(account_id)
    , equity_id INTEGER REFERENCES gl.equity(equity_id)
    , sector_composition_share NUMERIC(8,6) NOT NULL
    , sector_composition_from_date DATE NOT NULL
    , sector_composition_to_date DATE
    , sector_composition_current BOOLEAN NOT NULL
);
