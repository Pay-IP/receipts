import datetime
import random
from uuid import UUID
from pydantic import BaseModel

emv_transaction_date_format_str = '%Y%M%D' 
emv_transaction_time_format_str = '%H%M%S' 
emv_retrieval_reference_number_format_str = '%YY%M%D%H%M%S'

def random_card_pan_for_bin(bin: str, length: int = 16):
    suffix = ''.join(random.sample('0123456789', length - len(bin)))
    return f'{bin}{suffix}'

def formatted_transaction_date(
        timestamp: datetime.datetime,
        format_str = emv_transaction_date_format_str
) -> str:
    return timestamp.strftime(format_str)

def formatted_transaction_time(
        timestamp: datetime.datetime,
        format_str = emv_transaction_time_format_str
) -> str:
    return timestamp.strftime(format_str)

def formatted_system_trace_audit_number(stan: int) -> str:
    return str(stan).rjust(6, '0')

def formatted_terminal_serial_number(tsn: int) -> str:
    return str(tsn).rjust(5, '0')

def random_terminal_verification_results() -> str:
    return '0000000000'

def random_emv_CTQ() -> str:
    return '0000'

def random_emv_application_cryptogram() -> str:
    hex = ''.join(random.sample('0123456789ABCDEF', 14))
    return f'AC{hex}'

def formatted_unique_transaction_identifier(
    guid: UUID,
    card_acc_idc: str,
    formatted_terminal_serial_number: int
) -> str:
    
    card_acc_idc_len = len(card_acc_idc)
    card_acc_idc_target_len = 11
    cut_card_acc_idc = card_acc_idc[card_acc_idc_len - card_acc_idc_target_len:]

    return f'{guid}-{cut_card_acc_idc}-{formatted_terminal_serial_number}'

def formatted_retrieval_reference_number(
    timestamp: datetime.datetime
) -> str:
    return timestamp.strftime(emv_retrieval_reference_number_format_str)

class ISO8583_0200_FinReqMsg(BaseModel):

    transaction_date_str: str
    transaction_time_str: str    
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
    authorized: bool  
    authorization_response_identifier: str

class ISO8583_02_RqRsp(BaseModel):
    iso_0200_fin_req: ISO8583_0200_FinReqMsg
    iso_0210_fin_rsp: ISO8583_0210_FinRspMsg

class TerminalEmvReceipt(BaseModel):
    iso_0200_fin_req: ISO8583_0200_FinReqMsg
    iso_0210_fin_rsp: ISO8583_0210_FinRspMsg
