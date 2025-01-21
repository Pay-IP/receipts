from pydantic import BaseModel, validator


class NullRequest(BaseModel):
    pass

class TriggerRequest(BaseModel):
    pass

class TriggerResponse(BaseModel):
    rsp: str