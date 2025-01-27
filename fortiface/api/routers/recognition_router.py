from app.pipelines.process_pipline import Pipeline
from fastapi import APIRouter

from fortiface.schemas import ServiceRequest, ServiceResponse

router = APIRouter()


@router.post("/search", status_code=200, description="", response_model=ServiceResponse)
async def start_process(req: ServiceRequest):
    return Pipeline().invoke(req)


@router.get("/info", status_code=200, description="", response_model=ServiceResponse)
async def get_info():
    return Pipeline().get_info()
