# alembic/env.py
from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool
import os
import sys

# --- RUTA DEL PROYECTO ---
# Ajusta si tu estructura difiere (aquí asumimos repo_root/app/...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.join(BASE_DIR)  # repo_root/alembic/.. = repo_root
APP_DIR = os.path.join(PROJECT_ROOT, "app")
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

# Importa la Base que agrupa TODOS los modelos
from models import Base  # app/models/__init__.py expone Base

# --- Config Alembic ---
config = context.config

# Si tienes alembic.ini con: sqlalchemy.url = ${DATABASE_URL}
# y Railway inyecta DATABASE_URL, Alembic lo tomará de env.
# Si quieres forzar desde env cuando no está seteado en ini:
db_url = os.getenv("DATABASE_URL")
if db_url:
    config.set_main_option("sqlalchemy.url", db_url)

# Logging de Alembic
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata objetivo (¡clave!)
target_metadata = Base.metadata


def run_migrations_offline():
    """Ejecuta migraciones en modo 'offline' (sin DB conectada)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Ejecuta migraciones en modo 'online' (con DB conectada)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
