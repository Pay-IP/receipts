from pydantic import BaseModel

class NullRequest(BaseModel):
    pass

class StringResponse(BaseModel):
    rsp: str