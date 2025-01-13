
-- Client

CREATE TABLE merchant_client (

    id INTEGER GENERATED ALWAYS AS IDENTITY,
        PRIMARY KEY(id),

    platform_reference UUID NOT NULL UNIQUE
);

-- Payment Processor

CREATE TABLE merchant_payment_processor (

    id INTEGER GENERATED ALWAYS AS IDENTITY,
        PRIMARY KEY(id),

    name VARCHAR(254) NOT NULL UNIQUE,
    merchant_reference UUID NOT NULL UNIQUE
);


-- SKU

CREATE TABLE merchant_sku (

    id INTEGER GENERATED ALWAYS AS IDENTITY,
        PRIMARY KEY(id),

    name VARCHAR(254) NOT NULL UNIQUE,
    price INTEGER NOT NULL
);

-- Invoice

CREATE TABLE merchant_invoice (

    id INTEGER GENERATED ALWAYS AS IDENTITY,
        PRIMARY KEY(id),

    client_id INTEGER NULL,
    CONSTRAINT merchant_invoice_fk_client_id
        FOREIGN KEY(client_id) 
	    REFERENCES merchant_client(id), 

    timestamp TIMESTAMPTZ NOT NULL,

    currency_id INTEGER NOT NULL,
    CONSTRAINT fk_merchant_invoice_currency
        FOREIGN KEY(currency_id) 
	    REFERENCES currency(id),

    sales_tax_percent DECIMAL(10, 2),

    total_amount_before_tax INTEGER NOT NULL,
    sales_tax_amount INTEGER NOT NULL,
    total_amount_after_tax INTEGER NOT NULL
);

-- InvoiceLine

CREATE TABLE merchant_invoice_line (

    id INTEGER GENERATED ALWAYS AS IDENTITY,
        PRIMARY KEY(id),

    invoice_id INTEGER NOT NULL,
    CONSTRAINT merchant_invoice_line_fk_invoice_id
        FOREIGN KEY(invoice_id) 
	    REFERENCES merchant_invoice(id), 

    sku_id INTEGER NOT NULL,
    CONSTRAINT merchant_invoice_line_fk_sku_id
        FOREIGN KEY(sku_id) 
	    REFERENCES merchant_sku(id), 

    sku_count INTEGER NOT NULL,
    currency_amount INTEGER NOT NULL
);

-- InvoicePayment

CREATE TABLE merchant_invoice_payment (

    id INTEGER GENERATED ALWAYS AS IDENTITY,
        PRIMARY KEY(id),

    invoice_id INTEGER NOT NULL,
    CONSTRAINT merchant_invoice_payment_fk_invoice_id
        FOREIGN KEY(invoice_id) 
	    REFERENCES merchant_invoice(id), 

    timestamp TIMESTAMPTZ NOT NULL,

    currency_id INTEGER NOT NULL,
    CONSTRAINT fk_merchant_invoice_payment_currency
        FOREIGN KEY(currency_id) 
	    REFERENCES currency(id),
    currency_amount INTEGER NOT NULL,

    payment_processor_id INTEGER NOT NULL,
    CONSTRAINT merchant_sale_payment_fk_payment_processor_id
        FOREIGN KEY(payment_processor_id) 
	    REFERENCES merchant_payment_processor(id), 

    payment_processor_reference VARCHAR(254) NOT NULL,

    successful BOOLEAN NOT NULL
);


-- Invoice Receipt

CREATE TABLE merchant_invoice_receipt (

    id INTEGER GENERATED ALWAYS AS IDENTITY,
        PRIMARY KEY(id),

    invoice_id INTEGER NOT NULL,
    CONSTRAINT merchant_invoice_receipt_fk_invoice_id
        FOREIGN KEY(invoice_id) 
	    REFERENCES merchant_invoice(id)
);

