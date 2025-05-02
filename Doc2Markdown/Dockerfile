# Usa una imagen oficial de Python como base
FROM python:3.11-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo de dependencias
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el contenido del proyecto al contenedor
COPY . .

# Exponer el puerto que usará FastAPI
EXPOSE 8000

# Comando para correr la aplicación
CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
