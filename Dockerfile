# Imagen base
FROM python:3.11-slim

# Evita .pyc y fuerza stdout sin buffer
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Paquetes del sistema (mínimos)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc curl \
 && rm -rf /var/lib/apt/lists/*

# Carpeta de trabajo
WORKDIR /app

# Requisitos primero (mejor caché)
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código y archivos de alembic
COPY ./app ./app
COPY ./alembic ./alembic
COPY ./alembic.ini ./alembic.ini

# Variables útiles (puedes cambiarlas si tu módulo cambia)
ENV MODULE_NAME=app.main
ENV APP_MODULE=${MODULE_NAME}:app

# Expón el puerto localmente (Railway inyecta $PORT en runtime)
EXPOSE 8000

# Ejecuta migraciones y arranca uvicorn
# - Si no hay migraciones, imprime mensaje y continúa.
CMD ["sh", "-c", "alembic upgrade head || echo 'No migrations to apply'; uvicorn ${APP_MODULE} --host 0.0.0.0 --port ${PORT:-8000}"]
