DROP TABLE IF EXISTS gl.country_composition;

CREATE TABLE gl.country_composition (
      country_composition_id SERIAL PRIMARY KEY
    , country_id INTEGER REFERENCES gl.country(country_id)
    , equity_id INTEGER REFERENCES gl.equity(equity_id)
    , country_composition_share NUMERIC(8,6) NOT NULL
    , country_composition_from_date DATE NOT NULL
    , country_composition_to_date DATE
    , country_composition_current BOOLEAN NOT NULL
);
