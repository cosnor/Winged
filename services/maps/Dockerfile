# Imagen base# Imagen base
FROM python:3.12-slim

# Crear directorio de trabajo
WORKDIR /code

# Copiar requirements y instalar dependencias
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copiar todo el código de la aplicación
COPY ./app /code/app

# Exponer puerto de FastAPI
EXPOSE 8004

# Comando de inicio
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8004", "--reload"]