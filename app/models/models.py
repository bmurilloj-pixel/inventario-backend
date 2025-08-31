# app/models/models.py
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime,
    func,
)
from sqlalchemy.orm import relationship

# Importa la Base que definimos en app/__init__.py
from app import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user", nullable=False)
    local_kw = Column(String, nullable=True)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    quantity = Column(Float, default=0, nullable=False)
    price = Column(Float, default=0, nullable=False)

    # Relación inversa opcional si luego la necesitas:
    movements = relationship("Movement", back_populates="product", cascade="all, delete-orphan")
    inventory_items = relationship("Inventory", back_populates="product", cascade="all, delete-orphan")


class Movement(Base):
    __tablename__ = "movements"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), index=True, nullable=False)
    quantity = Column(Float, nullable=False)
    note = Column(String, nullable=True)
    timestamp = Column(DateTime, server_default=func.now(), nullable=False)

    product = relationship("Product", back_populates="movements")


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), index=True, nullable=False)
    quantity = Column(Float, nullable=False)
    note = Column(String, nullable=True)
    timestamp = Column(DateTime, server_default=func.now(), nullable=False)

    product = relationship("Product", back_populates="inventory_items")
