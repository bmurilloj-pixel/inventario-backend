from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core import database
from app.models import models
from app.utils.security import get_password_hash

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/create")
def create_user(username: str, password: str, role: str = "user", db: Session = Depends(database.SessionLocal)):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    hashed_password = get_password_hash(password)
    user = models.User(username=username, hashed_password=hashed_password, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"msg": "Usuario creado", "user": user.username}
