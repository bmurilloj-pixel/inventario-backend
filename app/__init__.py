# app/models/__init__.py
from sqlalchemy.orm import declarative_base

# La Base central que usarán todos los modelos
Base = declarative_base()

# Importa aquí TODOS tus modelos para que se registren en Base.metadata
# (ajusta los nombres según tus archivos reales)
from .user import User  # noqa: F401
from .inventory import Inventory  # noqa: F401
