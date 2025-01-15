from pydantic import BaseModel

class ISO8583_0200_FinReqMsg(BaseModel):

    transaction_date: str
    transaction_time: str    
    currency_code: str
    currency_amount: int
    
    pan: str

    emv_application_label: str
    application_ID: str
    CTQ: str
    terminal_verification_results: str
    application_cryptogram: str
    terminal_serial_number: str

    terminal_system_trace_audit_number: str
    unique_transaction_identifier: str
    retrieval_reference_number: str

    merchant_address: str


class ISO8583_0210_FinRspMsg(BaseModel):
    approved: bool  
    authorization_response_identifier: str

class ISO8583_02_Messages(BaseModel):
    iso_0200_fin_req: ISO8583_0200_FinReqMsg
    iso_0210_fin_rsp: ISO8583_0210_FinRspMsg

class TerminalEmvReceipt(BaseModel):
    iso_0200_fin_req: ISO8583_0200_FinReqMsg
    iso_0210_fin_rsp: ISO8583_0210_FinRspMsg
