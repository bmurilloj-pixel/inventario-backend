import os
from fastapi import FastAPI
from app.routers.users import router as users_router
from app.routers.auth import auth as auth_router

app = FastAPI(
    title="Inventario Vidrio",
    version="1.0.0",
    description="API para gestión de inventario de vidrio",
)

# Incluir routers
app.include_router(users_router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Inventario Vidrio API funcionando 🚀"}

if __name__ == "__main__":
    # Para correr localmente: uvicorn app.main:app --reload
    port = int(os.getenv("PORT", 8000))
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)
