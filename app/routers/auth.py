# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User

auth = APIRouter(prefix="/auth", tags=["Auth"])

class LoginBody(BaseModel):
    username: str
    password: str

@auth.post("/login")
def login(payload: LoginBody, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or user.hashed_password != payload.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "ok"}  # aquí devolver tu token si usas JWT
