from pydantic import BaseModel, Field

from fortiface.common.utils import datetime_now


class PersonBase(BaseModel):
    vector: list[float] = Field(
        ..., description="Vector representation of a person face."
    )


class PersonInDB(PersonBase):
    fullname: str = Field(..., description="")
    image_url: str = Field(..., description="")
    metadata: dict = Field(..., description="")
    created_at: int = Field(..., default_factory=datetime_now)
    modified_at: int = Field(..., default_factory=datetime_now)


class PersonUpdate(PersonInDB):
    pass


class PersonOutDB(PersonInDB):
    id: str
