from services.iss_bank_new_pmt.definition import issuing_bank_new_payment_service_definition
from util.service.service_base import start_service

if __name__ == '__main__':
    start_service(
        definition=issuing_bank_new_payment_service_definition()
    )