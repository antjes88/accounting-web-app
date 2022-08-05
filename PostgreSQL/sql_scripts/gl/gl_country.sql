DROP TABLE IF EXISTS gl.country;

CREATE TABLE gl.country (
      country_id SERIAL PRIMARY KEY
    , country_name VARCHAR(100) NOT NULL
    , country_continent VARCHAR(100) NOT NULL
    , country_economic_zone VARCHAR(100)
);