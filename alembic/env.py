from logging.config import fileConfig
import os
from urllib.parse import quote_plus

from sqlalchemy import engine_from_config, pool
from alembic import context

# IMPORTA EL Base QUE USA TU APP
#  - Si defines Base en app/core/database.py, importa desde ahí:
from app.core.database import Base
#  - Si lo defines en app/__init__.py, cambia a:
# from app import Base

# Objeto de configuración de Alembic
config = context.config

# Configuración de logging desde alembic.ini (si existe)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata objetivo para autogenerate
target_metadata = Base.metadata


def _build_database_url() -> str:
    """
    Igual que en database.py, pero inline para Alembic:
    intenta DATABASE_URL y si no, arma con variables PG* de Railway.
    Normaliza esquema y añade sslmode=require si aplica.
    """
    url = os.getenv("DATABASE_URL") or os.getenv("DATABASE_URI")

    if url:
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+psycopg2://", 1)
        elif url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+psycopg2://", 1)

        if "sslmode=" not in url and all(x not in url for x in ("localhost", "127.0.0.1")):
            url += ("&" if "?" in url else "?") + "sslmode=require"

        return url

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

    # Último recurso: lo que haya en alembic.ini (sqlalchemy.url)
    fallback = config.get_main_option("sqlalchemy.url")
    return fallback


def run_migrations_offline() -> None:
    """Ejecuta migraciones en modo 'offline' (sin abrir conexión real)."""
    url = _build_database_url()
    if not url:
        raise RuntimeError("No hay URL de base de datos configurada para Alembic.")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Ejecuta migraciones en modo 'online' usando una conexión real."""
    url = _build_database_url()
    if not url:
        raise RuntimeError("No hay URL de base de datos configurada para Alembic.")

    # Se inyecta en la config para que engine_from_config la use
    config.set_main_option("sqlalchemy.url", url)

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
