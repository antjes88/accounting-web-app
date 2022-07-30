DROP TABLE IF EXISTS gl.platform_account;

CREATE TABLE gl.platform_account (
      platform_account_id SERIAL PRIMARY KEY
    , platform_id INTEGER REFERENCES gl.platform(platform_id)
    , platform_account_name VARCHAR(255) NOT NULL
);
