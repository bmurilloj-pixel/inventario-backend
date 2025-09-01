from fastapi import FastAPI
from app.routers.users import router as users_router
from app.routers.auth import auth as auth_router

app = FastAPI(
    title="Inventario Vidrio",
    version="1.0.0",
    description="API para gestión de inventario de vidrio",
)

app.include_router(users_router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Inventario Vidrio API funcionando 🚀"}
