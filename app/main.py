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
