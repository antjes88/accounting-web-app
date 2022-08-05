DROP TABLE IF EXISTS gl.sector;

CREATE TABLE gl.sector (
      sector_id SERIAL PRIMARY KEY
    , sector_name VARCHAR(100) NOT NULL
);