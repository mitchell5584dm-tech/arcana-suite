from fastapi import APIRouter
from backend.app import run_command

router = APIRouter()

@router.post("/command")
def validate_command(payload: dict):
    return run_command(payload.get("cmd", ""))

