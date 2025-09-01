# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importa tus routers (ya definen sus propios prefijos dentro de cada archivo)
from app.routers.users import router as users_router
from app.routers.auth import auth as auth_router

app = FastAPI(
    title="Inventario Vidrio",
    version="1.0.0",
    description="API para gestión de inventario de vidrio",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# (Opcional) CORS permisivo; ajusta orígenes en producción
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # cambia por tus dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers de la aplicación
app.include_router(users_router)
app.include_router(auth_router)


@app.get("/", tags=["default"])
def root():
    """Endpoint básico para verificar que la API responde."""
    return {"message": "Inventario Vidrio API funcionando 🚀"}

@app.get("/health", tags=["default"])
def health():
    """Endpoint de salud para chequeos simples (Railway/monitores)."""
    return {"status": "ok"}
