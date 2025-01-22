from services.iss_bank_new_pmt.rqrsp import IssuingBankNewCardPaymentRequest
from services.trigger.rqrsp import NullRequest
from util.service.service_base import ServiceDefinition, api_for_service_definition
from util.service.service_base import request_handler
from services.iss_bank_new_pmt.logic import handle_get_issuing_bank_client_account_debits, handle_get_issuing_bank_client_accounts, handle_issuing_bank_new_payment_request_from_payment_processor
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

    @api.get("/issuing_bank_client_accounts")
    def get_issuing_bank_client_accounts(rq: NullRequest):
        return request_handler(
            definition,
            NullRequest,
            handle_get_issuing_bank_client_accounts
        )(rq)

    @api.get("/issuing_bank_client_account_debits")
    def get_issuing_bank_client_account_debits(rq: NullRequest):
        return request_handler(
            definition,
            NullRequest,
            handle_get_issuing_bank_client_account_debits
        )(rq)

    return api