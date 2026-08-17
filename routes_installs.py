from fastapi import APIRouter
from backend.app import install

router = APIRouter()

@router.post("/install")
def safe_install(config: dict):
    return install(config)

