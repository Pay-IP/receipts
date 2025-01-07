from services.merchant_pos_callback.definition import merchant_pos_callback_service_definition
from util.service.service_base import start_service

if __name__ == '__main__':
    start_service(
        definition=merchant_pos_callback_service_definition()
    )