-- =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
-- currency

CREATE TABLE currency (

    id INTEGER GENERATED ALWAYS AS IDENTITY,
        PRIMARY KEY(id),

    iso3 NCHAR(3) NOT NULL UNIQUE,

    decimal_places SMALLINT NOT NULL
        CHECK ((decimal_places > 0) AND (decimal_places <= 8)),

    symbol VARCHAR NOT NULL UNIQUE
);
