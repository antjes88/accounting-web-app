DROP TABLE IF EXISTS gl.currency;

CREATE TABLE gl.currency (
      currency_id SERIAL PRIMARY KEY
    , currency_name VARCHAR(100) NOT NULL
);
