from enum import Enum


class Service(Enum):
    CREATE_BUY_ORDER = 'create_buy_order'
    FETCH_BUY_ORDERS = 'fetch_buy_orders'
    BTC_PRICE = 'btc_price'
    
    MIGRATION = 'migration'
    READ_MODEL_SYNC = 'read_model_sync'

    MERCHANT_POS_NEW_CHECKOUT = 'merchant_pos_new_checkout'
    MERCHANT_POS_CALLBACK = 'merchant_pos_callback'

    PMT_PROC_NEW_PMT = 'pmt_proc_new_pmt'

    ISS_BANK_NEW_PMT = 'iss_bank_new_pmt'
    ISS_BANK_CALLBACK = 'iss_bank_callback'
    
    PLATFORM_NEW_PMT = 'platform_new_pmt'
    PLATFORM_NEW_RECEIPT = 'platform_new_receipt'
    PLATFORM_MATCHING = 'platform_matching'

    TRIGGER = 'trigger'
