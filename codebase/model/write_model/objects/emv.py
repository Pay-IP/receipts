from pydantic import BaseModel

class AcquirerEmvTransactionData(BaseModel):

    date: str
    time: str    
    currency_code: str
    total: int
    
    pan: str

    emv_application_label: str
    AID: str
    CTQ: str
    TVR: str
    AC: str
    terminal_serial_number: str

    terminal_system_trace_audit_number: str
    unique_transaction_identifier: str
    retrieval_reference_number: str

    merchant_address: str


class IssuerEmvTransactionData(BaseModel):

    approved: bool  
    authorization_rsp_id: str
