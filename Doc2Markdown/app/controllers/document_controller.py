from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import FileResponse
from typing import Optional
import os
from pathlib import Path
from jose import JWTError, jwt
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.document_model import Document
from app.models.document_version_model import DocumentVersion
from app.models.conversion_log_model import ConversionLog
from app.models.user_model import User
from app.utils.document_converter import DocumentConverter
from app.utils.file_handler import FileHandler
from app.utils.navigation_generator import NavigationGenerator
from config.database import get_db
from config.config import Config

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/token")

# Función para obtener el user_id del token JWT
def get_user_from_token(token: str = Depends(oauth2_scheme)) -> int:
    try:
        # Decodificar el token
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=403, detail="No se pudo determinar el usuario del token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=403, detail="Token inválido")
    
@router.post("/upload/")
async def upload_document(
    file: UploadFile = File(...),
    title: str = Form(...),
    user_id: int = Depends(get_user_from_token),
    db: Session = Depends(get_db)
):
    # Verificar usuario
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Guardar archivo
    saved_file = await FileHandler.save_uploaded_file(file) 
    if not saved_file:
        raise HTTPException(status_code=400, detail="Tipo de archivo no permitido")
    
    filename, filepath = saved_file
    original_format = FileHandler.get_file_extension(filename)
    
    # Convertir a Markdown
    markdown_content = DocumentConverter.convert_to_markdown(filepath, original_format)
    if not markdown_content:
        raise HTTPException(status_code=500, detail="Error al convertir el documento")
    
    # Guardar en base de datos
    new_document = Document(
        user_id=user_id,
        title=title,
        original_format=original_format,
        markdown_content=markdown_content
    )
    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    
    # Crear versión inicial
    new_version = DocumentVersion(
        document_id=new_document.document_id,
        version_number=1,
        content=markdown_content
    )
    db.add(new_version)
    
    # Registrar log de conversión
    new_log = ConversionLog(
        document_id=new_document.document_id,
        status="SUCCESS",
        conversion_type=f"{original_format.upper()} to MD"
    )
    db.add(new_log)
    
    db.commit()
    
    # Generar archivos de navegación
    documents = db.query(Document).filter(Document.user_id == user_id).all()
    docs_data = [{"document_id": doc.document_id, "title": doc.title} for doc in documents]
    NavigationGenerator.generate_sidebar(docs_data, Config.UPLOAD_FOLDER)
    NavigationGenerator.generate_footer(Config.UPLOAD_FOLDER)
    
    return {
        "document_id": new_document.document_id,
        "title": new_document.title,
        "markdown_content": new_document.markdown_content
    }

@router.get("/download/{document_id}")
async def download_document(document_id: int, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.document_id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    
    # Crear archivo temporal Markdown
    temp_dir = os.path.join(Config.UPLOAD_FOLDER, "temp")
    os.makedirs(temp_dir, exist_ok=True)
    filename = f"document_{document_id}.md"
    filepath = os.path.join(temp_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(document.markdown_content)
    
    return FileResponse(
        filepath,
        media_type="text/markdown",
        filename=filename
    )



@router.get("/list/")
async def list_user_documents(user_id: int = Depends(get_user_from_token), db: Session = Depends(get_db)):
    # Verificar usuario
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Obtener documentos del usuario
    documents = db.query(Document).filter(Document.user_id == user_id).all()
    
    if not documents:
        raise HTTPException(status_code=404, detail="No se encontraron documentos para este usuario")
    
    # Formatear los documentos
    documents_data = [
        {"document_id": doc.document_id, "title": doc.title, "original_format": doc.original_format}
        for doc in documents
    ]
    
    return {"documents": documents_data}