import os
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()


def _build_database_url() -> str:
    """
    Obtiene la URL de la base de datos desde:
      1) DATABASE_URL / DATABASE_URI (si existe)
      2) Variables de Railway/PG: PGUSER, PGPASSWORD, PGHOST, PGPORT, PGDATABASE
    Normaliza el esquema a postgresql+psycopg2 y añade ?sslmode=require
    cuando no es localhost.
    """
    url = os.getenv("DATABASE_URL") or os.getenv("DATABASE_URI")

    if url:
        # Normalizar esquema para SQLAlchemy 2.x con psycopg2
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+psycopg2://", 1)
        elif url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+psycopg2://", 1)

        # Forzar SSL en entornos gestionados (Railway) si no está presente
        if "sslmode=" not in url and all(x not in url for x in ("localhost", "127.0.0.1")):
            url += ("&" if "?" in url else "?") + "sslmode=require"

        return url

    # Construcción manual desde variables de Railway
    user = os.getenv("PGUSER")
    password = os.getenv("PGPASSWORD")
    host = os.getenv("PGHOST") or os.getenv("POSTGRES_HOST")
    port = os.getenv("PGPORT") or "5432"
    db = os.getenv("PGDATABASE") or os.getenv("POSTGRES_DB") or "railway"

    if user and password and host:
        return (
            f"postgresql+psycopg2://{quote_plus(user)}:{quote_plus(password)}"
            f"@{host}:{port}/{db}?sslmode=require"
        )

    raise RuntimeError(
        "No se encontró DATABASE_URL ni variables PG* necesarias "
        "(PGUSER/PGPASSWORD/PGHOST/PGPORT/PGDATABASE)."
    )


DATABASE_URL = _build_database_url()

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    future=True,
)


def get_db():
    """
    Dependencia para FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
