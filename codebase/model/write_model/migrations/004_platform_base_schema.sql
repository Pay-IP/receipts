-- =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
-- platform_merchant

CREATE TABLE platform_merchant (

    id INTEGER GENERATED ALWAYS AS IDENTITY,
        PRIMARY KEY(id),

    name VARCHAR(254) NOT NULL UNIQUE
);

-- =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
-- platform_merchant_config

CREATE TABLE platform_merchant_config (

    id INTEGER GENERATED ALWAYS AS IDENTITY,
        PRIMARY KEY(id),

    merchant_id INTEGER NOT NULL,
    CONSTRAINT fk_platform_merchant_config_merchant_id
        FOREIGN KEY(merchant_id) 
	    REFERENCES platform_merchant(id),

    merchant_address VARCHAR(254) NOT NULL UNIQUE,
    merchant_categorisation_code NCHAR(4) NOT NULL UNIQUE
);

-- =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
-- platform_bank

CREATE TABLE platform_bank (

    id INTEGER GENERATED ALWAYS AS IDENTITY,
        PRIMARY KEY(id),

    name VARCHAR NOT NULL UNIQUE
);

-- =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
-- platform_bank_config

CREATE TABLE platform_bank_config (

    id INTEGER GENERATED ALWAYS AS IDENTITY,
        PRIMARY KEY(id),

    bank_id INTEGER NOT NULL,
    CONSTRAINT fk_platform_bank_config_bank_id
        FOREIGN KEY(bank_id) 
	    REFERENCES platform_bank(id),

    card_bin VARCHAR(6) NOT NULL UNIQUE
);


-- =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
-- platform_bank_client_ac

CREATE TABLE platform_bank_client_ac (

    id INTEGER GENERATED ALWAYS AS IDENTITY,
        PRIMARY KEY(id),

    bank_id INTEGER NOT NULL,
    CONSTRAINT fk_platform_bank_client_ac_bank_id
        FOREIGN KEY(bank_id) 
	    REFERENCES platform_bank(id),

    source_system_id UUID NOT NULL
);

-- =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
-- platform_bank_client_ac_meta_data

CREATE TABLE platform_bank_client_ac_meta_data (

    id INTEGER GENERATED ALWAYS AS IDENTITY,
        PRIMARY KEY(id),

    bank_client_ac_id INTEGER NOT NULL,
    CONSTRAINT fk_platform_bank_client_ac_meta_data_platform_bank_client_ac_id
        FOREIGN KEY(bank_client_ac_id) 
	    REFERENCES platform_bank_client_ac(id),

    client_age INTEGER NULL,
    client_postal_code VARCHAR(64) NULL
);

-- =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
-- platform_bank_client_ac_payment

CREATE TABLE platform_bank_client_ac_payment (

    id INTEGER GENERATED ALWAYS AS IDENTITY,
        PRIMARY KEY(id),

    bank_client_ac_id INTEGER NOT NULL,
    CONSTRAINT fk_platform_bank_client_ac_payment_bank_client_ac_id
        FOREIGN KEY(bank_client_ac_id) 
	    REFERENCES platform_bank_client_ac(id),

    system_timestamp TIMESTAMPTZ NOT NULL,
    source_system_id UUID NOT NULL,
    payment JSON
);

-- =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
-- platform_merchant_receipt

CREATE TABLE platform_merchant_receipt (

    id INTEGER GENERATED ALWAYS AS IDENTITY,
        PRIMARY KEY(id),
    external_id UUID NOT NULL,
    source_system_id UUID NOT NULL,

    merchant_id INTEGER NOT NULL,
    CONSTRAINT fk_platform_merchant_receipt_merchant_id
        FOREIGN KEY(merchant_id) 
	    REFERENCES platform_merchant(id),

    system_timestamp TIMESTAMPTZ NOT NULL,
    receipt JSON
);

-- =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
-- platform_merchant_receipt_for_bank_client_ac_payment 

CREATE TABLE platform_match_merchant_receipt_to_bank_client_ac_payment (

    id INTEGER GENERATED ALWAYS AS IDENTITY,
        PRIMARY KEY(id),

    merchant_receipt_id INTEGER NOT NULL,
    CONSTRAINT fk_platform_merchant_receipt_for_bank_client_ac_payment_merchant_receipt_id
        FOREIGN KEY(merchant_receipt_id) 
	    REFERENCES platform_merchant_receipt(id),

    bank_client_ac_payment_id INTEGER NOT NULL,
    CONSTRAINT fk_platform_merchant_receipt_for_bank_client_ac_payment_bank_client_ac_payment_id
        FOREIGN KEY(bank_client_ac_payment_id) 
	    REFERENCES platform_bank_client_ac_payment(id),

    timestamp TIMESTAMPTZ NOT NULL
);