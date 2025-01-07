from services.iss_bank_callback.definition import issuing_bank_callback_service_definition
from util.service.service_base import start_service

if __name__ == '__main__':
    start_service(
        definition=issuing_bank_callback_service_definition()
    )