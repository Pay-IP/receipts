from services.pmt_proc_new_pmt.definition import payment_processor_new_payment_service_definition
from util.service.service_base import start_service

if __name__ == '__main__':
    start_service(
        definition=payment_processor_new_payment_service_definition()
    )