from services.platform_new_receipt.definition import platform_new_receipt_service_definition
from util.service.service_base import start_service

if __name__ == '__main__':
    start_service(
        definition=platform_new_receipt_service_definition()
    )