# Merchant
# - id
# - name
# - URL

# IssuingBank
# - id
# - name
# - URL

# Transaction
# - id
# - timestamp
# - merchant_id
# - issuing_bank_id
# - total
# - currency
# - reference


from sqlalchemy import Column, Integer, DateTime, String, SMALLINT
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from model.write_model.objects.write_model_base import WriteModelBase