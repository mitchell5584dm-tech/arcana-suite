from fastapi import APIRouter
from backend.app import subscription

router = APIRouter()

@router.get("/subscription/{plan_id}")
def get_subscription(plan_id: str):
    return subscription(plan_id)

