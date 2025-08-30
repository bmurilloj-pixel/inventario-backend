# Imagen base
FROM python:3.11-slim

# Evita .pyc y fuerza stdout sin buffer
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=10000

# Dependencias del sistema (psycopg2, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Workdir
WORKDIR /code

# Requisitos primero (mejor caché)
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt

# Copia del código
COPY ./app /code/app

# Expón el puerto local (opcional, útil para claridad)
EXPOSE 10000

# Ejecuta uvicorn apuntando a app.main:app
# Usa el PORT de Railway si existe; si no, 10000
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}"]
