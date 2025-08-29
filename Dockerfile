FROM python:3.11-slim

# 1) Directorio de trabajo dentro del contenedor
WORKDIR /code

# 2) Dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3) Código
COPY . .

# 4) Asegura que Python pueda importar desde /code
ENV PYTHONPATH=/code

# 5) Arranque con Uvicorn (expande $PORT de Railway)
#   (shell form -> expande variables)
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}
