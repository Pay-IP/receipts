from services.merchant_pos_new_checkout.definition import merchant_pos_new_checkout_service_definition
from util.service.service_base import start_service

if __name__ == '__main__':
    start_service(
        definition=merchant_pos_new_checkout_service_definition()
    )