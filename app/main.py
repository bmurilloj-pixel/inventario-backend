from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, users, inventory

app = FastAPI(title="Inventario Vidrio")

# ==== CORS (muy importante para que Netlify pueda llamar a Railway) ====
# Cambia este dominio por el de TU sitio en Netlify si no coincide.
ALLOWED_ORIGINS = [
    "https://serene-trifle-9155ae.netlify.app",  # tu frontend en Netlify
    # Opcionales para desarrollo local:
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ======================================================================

# Rutas principales (tus routers ya definidos)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(inventory.router)

@app.get("/")
def root():
    return {"message": "Backend Inventario Vidrio funcionando 🚉"}
import os
import httpx
from fastapi.middleware.cors import CORSMiddleware

# ⚙️ CORS para permitir llamadas desde tu Netlify
# Reemplaza por tu dominio Netlify (o añade más dominios si los tienes)
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://serene-trifle-9155ae.netlify.app")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],   # o ["*"] si prefieres permitir todo (menos seguro)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📦 Puerto en Railway (por defecto 8080)
PORT = int(os.getenv("PORT", 8080))

@app.on_event("startup")
async def seed_admin_user():
    """
    Crea (si no existe) un usuario ADMIN al iniciar el servidor,
    llamando al propio endpoint /users/create
    """
    params = {
        "username": "ADMIN",
        "password": "1234",
        "role": "admin",
        # Este parámetro lo vi en tu Swagger como requerido.
        # Ponle cualquier string válido que tu endpoint acepte.
        "local_kw": "seed",  
    }

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(f"http://127.0.0.1:{PORT}/users/create", params=params)
            # No importa si “ya existe”; imprimimos para depurar
            print(f"🔹 Seed admin response: {resp.status_code} {resp.text[:200]}")
    except Exception as e:
        print(f"⚠️ Error sembrando usuario ADMIN: {e}")
from app.core.database import Base, engine
from app.models import user, inventory  # importa todos tus modelos aquí

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)
