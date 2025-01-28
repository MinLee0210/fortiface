from fastapi import APIRouter, HTTPException

from fortiface.schemas.register_schemas import (PersonBase, PersonInDB,
                                                PersonOutDB, PersonUpdate)
from fortiface.services.register_services import register_service

router = APIRouter()


@router.post("/search", status_code=200)
def search_vector(data: PersonBase, limit: int = 1, search_params: dict = {}):
    resp = register_service.search(data=data, limit=limit, search_params=search_params)
    if not resp.get("success"):
        raise HTTPException(status_code=422, detail=resp.get("detail"))
    return resp.get("data")


@router.post("", status_code=201)
def create_vector(data: PersonInDB):
    resp = register_service.insert(data=data)
    if not resp.get("success"):
        raise HTTPException(status_code=422, detail=resp.get("detail"))
    return resp.get("data")


@router.get("/{identity_id}", status_code=200)
def get_identity_by_id(identity_id: str):
    resp = register_service.get_identity(identity_id=identity_id)
    if not resp.get("success"):
        raise HTTPException(status_code=422, detail=resp.get("detail"))
    return resp.get("data")


@router.put("/{identity_id}", status_code=200)
def update_identity(identity_id: str, data: PersonUpdate):
    resp = register_service.update_identity(identity_id=identity_id, data=data)
    if not resp.get("success"):
        raise HTTPException(status_code=422, detail=resp.get("detail"))
    return resp.get("data")


@router.delete("/identity/{identity_id}", status_code=200)
def delete_vector(identity_id: str):
    resp = register_service.delete_identity(identity_id=identity_id)
    if not resp.get("success"):
        raise HTTPException(status_code=422, detail=resp.get("detail"))
    return resp.get("success")
