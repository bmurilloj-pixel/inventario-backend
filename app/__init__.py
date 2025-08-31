# app/__init__.py
from sqlalchemy.orm import declarative_base

# Base central que usarán todos los modelos
Base = declarative_base()

# Importa los modelos para que se registren en Base.metadata
# (Importar al final para evitar ciclos de importación)
from .models.models import User, Product, Movement, Inventory  # noqa: F401
