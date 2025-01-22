from pydantic import BaseModel

class StringResponse(BaseModel):
    rsp: str