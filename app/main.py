from fastapi import FastAPI
from app.routers import auth, users, inventory

# Inicialización de la app con documentación habilitada
app = FastAPI(
    title="Inventario Vidrio",
    description="API para gestión de inventario de vidrio",
    version="1.0.0",
    docs_url="/docs",      # Habilita Swagger UI
    redoc_url="/redoc"     # Habilita ReDoc
)

# Rutas principales
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(inventory.router)

# Ruta raíz
@app.get("/")
def root():
    return {"message": "Backend Inventario Vidrio funcionando 🚀"}
