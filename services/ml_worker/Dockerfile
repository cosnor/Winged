# services/ml_worker/Dockerfile
FROM python:3.12-slim

# Crear directorio de trabajo
WORKDIR /code

# Instalar dependencias del sistema si hacen falta (ejemplo: numpy, scipy, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements si lo tienes
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del worker
COPY . /code

# Comando por defecto (ajústalo a tu caso)
# Si tu worker es un script que se queda escuchando o corriendo en loop:
CMD ["python", "app/worker.py"]
