#!/bin/bash

# Ejecutar la aplicación con gunicorn + uvicorn.worker
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.app:app --bind=0.0.0.0 --timeout 300
