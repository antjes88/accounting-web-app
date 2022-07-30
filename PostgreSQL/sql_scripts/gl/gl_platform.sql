DROP TABLE IF EXISTS gl.platform;

CREATE TABLE gl.platform (
      platform_id SERIAL PRIMARY KEY
    , country_id INTEGER REFERENCES gl.country(country_id)
    , platform_name VARCHAR(255) NOT NULL
    , platform_description VARCHAR(511) NOT NULL
    , platform_web_page VARCHAR(255)
);
