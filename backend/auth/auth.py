from fastapi import APIRouter, HTTPException, Form
from backend.auth.jwt import create_token

router = APIRouter()

@router.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "123":
        token = create_token({"sub": username})
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")
