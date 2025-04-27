from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.controllers.document_controller import router as document_router
from app.controllers.user_controller import router as user_router
from config.database import Base, engine
from config.config import Config
import os

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Inicializar app
app = FastAPI(
    title="Doc2Markdown API",
    description="API para convertir documentos a Markdown",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar rutas de API
app.include_router(document_router, prefix="/api/documents", tags=["documents"])
app.include_router(user_router, prefix="/api/users", tags=["users"])

# Montar archivos estáticos (CSS, JS, imágenes, documentos)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/uploads", StaticFiles(directory=Config.UPLOAD_FOLDER), name="uploads")

# Configurar plantillas Jinja2
templates = Jinja2Templates(directory="app/templates")

# Crear directorio uploads si no existe
@app.on_event("startup")
async def startup_event():
    if not os.path.exists(Config.UPLOAD_FOLDER):
        os.makedirs(Config.UPLOAD_FOLDER)

# Rutas Frontend
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/document_conversion", response_class=HTMLResponse)
async def document_conversion_page(request: Request):
    return templates.TemplateResponse("document_conversion.html", {"request": request})

# Ruta alternativa en caso de que alguien consulte /api root
@app.get("/api", response_class=HTMLResponse)
async def api_home(request: Request):
    return RedirectResponse(url="/")
