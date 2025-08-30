# Imagen base
FROM python:3.11-slim

# Ajustes de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Directorio de trabajo
WORKDIR /code

# Instalar dependencias del sistema si luego las necesitas (comentado por ahora)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential curl && \
#     rm -rf /var/lib/apt/lists/*

# Copiar requirements primero para cachear la capa de dependencias
COPY requirements.txt /code/requirements.txt
RUN pip install --upgrade pip && pip install -r /code/requirements.txt

# Copiar el código de la app (asumiendo carpeta /app en la raíz del repo)
COPY app /code/app

# (Opcional) Exponer el puerto
EXPOSE 8080

# Comando de arranque (muy importante el módulo: app.main:app)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
