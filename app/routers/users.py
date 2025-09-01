# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.core.database import get_db  # ajusta el import según tu proyecto
from app.models.models import User    # ajusta el import según tu proyecto

router = APIRouter(prefix="/users", tags=["Users"])

# --- Pydantic schema para el body ---
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=3)  # en prod: hashea
    role: str = Field(..., regex="^(admin|user)$")
    local_kw: str

@router.post("/create")
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    # ¿Usuario ya existe?
    existing = db.query(User).filter(User.username == payload.username).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )

    # Crea usuario (⚠️ para prod: hashear password)
    new_user = User(
        username=payload.username,
        hashed_password=payload.password,  # si tu columna se llama hashed_password
        role=payload.role,
        local_kw=payload.local_kw
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully", "username": new_user.username}
