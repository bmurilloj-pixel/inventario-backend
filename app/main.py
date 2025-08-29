from fastapi import FastAPI
from app.routers import auth, users, inventory

app = FastAPI(title="Inventario Vidrio")

# Rutas principales
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(inventory.router)

@app.get("/")
def root():
    return {"message": "Backend Inventario Vidrio funcionando 🚀"}
