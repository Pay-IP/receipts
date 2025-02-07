from uuid import UUID
from pydantic import BaseModel

def convert_uuids(obj):
    # Check if the object is a Pydantic model instance.
    if isinstance(obj, BaseModel):
        # Convert the model to a dict first.
        return convert_uuids(obj.model_dump())
    elif isinstance(obj, dict):
        return {k: convert_uuids(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_uuids(item) for item in obj]
    elif isinstance(obj, UUID):
        return str(obj)
    else:
        return obj
