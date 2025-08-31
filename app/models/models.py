from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    quantity = Column(Float, default=0)
    cost = Column(Float, default=0)
    price = Column(Float, default=0)

class Movement(Base):
    __tablename__ = "movements"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Float)
    type = Column(String)  # entrada o salida
    date = Column(DateTime, default=datetime.datetime.utcnow)
    product = relationship("Product")
# app/models.py
from sqlalchemy import Column, Integer, String, DateTime, func
from app.models import Base  # importa la Base del package

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="user")
    local_kw = Column(String, nullable=True)

class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    note = Column(String, nullable=True)
    timestamp = Column(DateTime, server_default=func.now(), nullable=False)
