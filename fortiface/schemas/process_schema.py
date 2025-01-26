from app.common.utils.utils import datetime_now
from pydantic import BaseModel


class ServiceRequest(BaseModel):
    payload: str | list[str] | object
    # add new field here

    timestamp: int = datetime_now()


class ServiceResponse(BaseModel):
    payload: str | list[str] | object

    timestamp: int = datetime_now()
