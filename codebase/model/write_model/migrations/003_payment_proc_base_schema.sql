-- =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
-- payment_processor_merchant

CREATE TABLE payment_processor_merchant (

    id INTEGER GENERATED ALWAYS AS IDENTITY,
        PRIMARY KEY(id),

    name VARCHAR(254) NOT NULL UNIQUE,
    address VARCHAR NOT NULL UNIQUE,

    currency_id INTEGER NOT NULL,
    CONSTRAINT fk_payment_processor_merchant_currency_id
        FOREIGN KEY(currency_id) 
	    REFERENCES currency(id)
);

-- =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
-- payment_processor_merchant_tsn

CREATE TABLE payment_processor_merchant_tsn (

    tsn SERIAL PRIMARY KEY,

    merchant_id INTEGER NOT NULL,
    CONSTRAINT fk_payment_processor_merchant_payment_merchant_id
        FOREIGN KEY(merchant_id) 
	    REFERENCES payment_processor_merchant(id)
);

-- =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
-- payment_processor_system_trace_audit_number

CREATE TABLE payment_processor_system_trace_audit_number (

    stan SERIAL PRIMARY KEY
);

-- =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
-- payment_processor_merchant_payment

CREATE TABLE payment_processor_merchant_payment (

    id INTEGER GENERATED ALWAYS AS IDENTITY,
        PRIMARY KEY(id),

    merchant_id INTEGER NOT NULL,
    CONSTRAINT fk_payment_processor_merchant_payment_merchant_id
        FOREIGN KEY(merchant_id) 
	    REFERENCES payment_processor_merchant(id),

    terminal_serial_number SERIAL
);


