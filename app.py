from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="ARCANA Suite Demo")

class TokenState(BaseModel):
    user_id: str
    tokens: int
    tower_height: int

FAKE_DB = {}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/token-state")
def update_token_state(state: TokenState):
    FAKE_DB[state.user_id] = state
    return {"ok": True, "state": state}

@app.get("/token-state/{user_id}")
def get_token_state(user_id: str):
    if user_id not in FAKE_DB:
        raise HTTPException(status_code=404, detail="Not found")
    return FAKE_DB[user_id]
