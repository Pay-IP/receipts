-- =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
-- issuing_bank_client_account

CREATE TABLE issuing_bank_client_account (

    id INTEGER GENERATED ALWAYS AS IDENTITY,
        PRIMARY KEY(id),

    name VARCHAR(254) NOT NULL,
    date_of_birth DATE NOT NULL,
    postal_code VARCHAR(254) NOT NULL,

    currency_id INTEGER NOT NULL,
    CONSTRAINT fk_issuing_bank_client_account_currency_id
        FOREIGN KEY(currency_id) 
	    REFERENCES currency(id),

    external_id UUID NOT NULL UNIQUE,

    card_pan VARCHAR(19) NOT NULL UNIQUE,
    card_aid VARCHAR(32) NOT NULL,
    card_app_label VARCHAR(20) NOT NULL
);

-- =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
-- issuing_bank_client_account_debit

CREATE TABLE issuing_bank_client_account_debit (

    id INTEGER GENERATED ALWAYS AS IDENTITY,
        PRIMARY KEY(id),
    external_id UUID NOT NULL UNIQUE,
    platform_payment_id UUID NULL UNIQUE,

    client_account_id INTEGER NOT NULL,
    CONSTRAINT fk_issuing_bank_client_account_debit_client_account_id
        FOREIGN KEY(client_account_id) 
	    REFERENCES issuing_bank_client_account(id),

    currency_amount INTEGER NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,

    platform_receipt_id UUID NULL,
    platform_receipt JSONB NULL,

    emv_rq JSONB,
    emv_rsp JSONB
);