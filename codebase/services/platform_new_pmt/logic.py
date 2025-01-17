from services.platform_new_pmt.rqrsp import PlatformNewPaymentRequest, PlatformNewPaymentResponse
from util.service.service_config_base import ServiceConfig

def handle_platform_new_payment_request_from_customer_bank(
    config: ServiceConfig,
    rq: PlatformNewPaymentRequest
):
    
    # model
    #
    # receipt side
    # - merchant 
    # - merchant receipt with payment details

    # payment side
    # - customer_ac (id obtained from bankZ)
    # - (customer) payment
    #
    # - customer account = our identity for the customer
    # - merchant payment


    return PlatformNewPaymentResponse(
        successful=True
    )