from pydantic import BaseModel, Field


class FortiFaceRequest(BaseModel): ...


class FortifaceResponse(BaseModel):
    id: str
    fullname: str = Field(..., description="")
    image_url: str = Field(..., description="")
    metadata: dict = Field(..., description="")
    detection_rate: float
    recognition_rate: float
    created_at: int
