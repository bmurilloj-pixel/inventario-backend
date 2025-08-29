from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core import database
from app.models import models

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.post("/entrada")
def add_entry(product_id: int, quantity: float, db: Session = Depends(database.SessionLocal)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product:
        product.quantity += quantity
        db.commit()
        return {"msg": "Entrada registrada", "product": product.name, "new_qty": product.quantity}
    return {"error": "Producto no encontrado"}

@router.post("/salida")
def remove_entry(product_id: int, quantity: float, db: Session = Depends(database.SessionLocal)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product and product.quantity >= quantity:
        product.quantity -= quantity
        db.commit()
        return {"msg": "Salida registrada", "product": product.name, "new_qty": product.quantity}
    return {"error": "Cantidad insuficiente o producto no encontrado"}
