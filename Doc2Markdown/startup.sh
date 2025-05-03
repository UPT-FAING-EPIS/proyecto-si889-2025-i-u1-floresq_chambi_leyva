#!/bin/bash

# Navegar al directorio donde está la aplicación
cd /home/site/wwwroot

# Instalar las dependencias si es necesario
pip install --no-cache-dir -r requirements.txt

# Ejecutar la aplicación con uvicorn a través del script run.py
python run.py
