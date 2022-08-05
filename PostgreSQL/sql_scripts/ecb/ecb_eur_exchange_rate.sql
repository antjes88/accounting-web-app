DROP TABLE IF EXISTS ecb.eur_exchange_rate;

CREATE TABLE ecb.eur_exchange_rate
(
	  eur_exchange_rate_id SERIAL PRIMARY KEY
	, eur_exchange_rate_date DATE UNIQUE
	, eur_exchange_rate_to_gbp NUMERIC(10,4) NOT NULL
	, eur_exchange_rate_to_dollar NUMERIC(10,4) NOT NULL
	, eur_exchange_rate_created_date TIMESTAMP WITH TIME ZONE NOT NULL
	, eur_exchange_rate_created_by VARCHAR(100) NOT NUll
);
