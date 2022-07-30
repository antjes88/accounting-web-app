DROP TABLE IF EXISTS gl.account;

CREATE TABLE gl.account (
      account_id SERIAL PRIMARY KEY
    , account_name VARCHAR(255) NOT NULL
    , account_description VARCHAR(511) NOT NULL
);
