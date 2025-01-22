from services.iss_bank_new_pmt.rqrsp import IssuingBankNewCardPaymentRequest
from util.service.service_base import ServiceDefinition, api_for_service_definition
from util.service.service_base import request_handler
from services.iss_bank_new_pmt.logic import handle_get_issuing_bank_client_account_by_id, handle_get_issuing_bank_client_account_debit_by_id, handle_get_issuing_bank_client_account_debits, handle_get_issuing_bank_client_accounts, handle_issuing_bank_new_payment_request_from_payment_processor
from services.iss_bank_new_pmt.definition import issuing_bank_new_payment_service_definition


def api():

    definition: ServiceDefinition = issuing_bank_new_payment_service_definition()    
    api = api_for_service_definition(definition)

    @api.post("/")
    def new_payment(rq: IssuingBankNewCardPaymentRequest):
        return request_handler(
            definition,
            IssuingBankNewCardPaymentRequest,
            handle_issuing_bank_new_payment_request_from_payment_processor
       )(rq)
    
    # these methods are here for convenience for internal testing
    # NOT FOR PRODUCTION USE - move to dedicated microservice

    @api.get("/client_accounts")
    def get_issuing_bank_client_accounts(id):
        return request_handler(
            definition,
            None,
            handle_get_issuing_bank_client_accounts
        )()


    @api.get("/client_account/{id}")
    def get_issuing_bank_client_account_by_id(id):
        return request_handler(
            definition,
            None,
            handle_get_issuing_bank_client_account_by_id
        )(id)

    @api.get("/client_account_debits")
    def get_issuing_bank_client_account_debits():
        return request_handler(
            definition,
            None,
            handle_get_issuing_bank_client_account_debits
        )()


    @api.get("/client_account_debit/{id}")
    def get_issuing_bank_client_account_debit_by_id(id):
        return request_handler(
            definition,
            None,
            handle_get_issuing_bank_client_account_debit_by_id
        )(id)

    return api