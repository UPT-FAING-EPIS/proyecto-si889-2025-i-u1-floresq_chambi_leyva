import uvicorn
from app.app import app

if __name__ == "__main__":
    uvicorn.run(
    "app.app:app",
    host="0.0.0.0",  # Cambiar a 0.0.0.0 en producción
    port=8000,
    reload=False  # Deshabilitar recarga en producción
)
    
# CONFIGURACION LOCAL
#   import uvicorn
#from app.app import app

#if _name_ == "_main_":
#    uvicorn.run(
#        "app.app:app",
#        host="127.0.0.1",
#        port=8000,
#        reload=True
#        #ssl_keyfile="./key.pem",
#        #ssl_certfile="./cert.pem"
    )