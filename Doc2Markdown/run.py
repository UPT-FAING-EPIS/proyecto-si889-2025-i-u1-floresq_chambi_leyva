import uvicorn
from app.app import app

if __name__ == "__main__":
    uvicorn.run(
    "app.app:app",
    host="0.0.0.0",  # Cambiar a 0.0.0.0 en producción
    port=8000,
    reload=False  # Deshabilitar recarga en producción
)