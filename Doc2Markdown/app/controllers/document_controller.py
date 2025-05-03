from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import FileResponse
from typing import Optional
import os
from pathlib import Path
from jose import JWTError, jwt
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.document_model import Document
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
    
    # Buscar documentos existentes con el mismo título
    existing_document = db.query(Document).filter(
        Document.user_id == user_id,
        Document.title == title
    ).order_by(Document.version.desc()).first()
    
    # Determinar el número de versión
    if existing_document:
        # Si existe, incrementar la versión máxima
        version_number = existing_document.version + 1
    else:
        # Si no existe, empezar con la versión 1
        version_number = 1
    
    # Guardar en base de datos
    new_document = Document(
        user_id=user_id,
        title=title,
        original_format=original_format,
        markdown_content=markdown_content,
        version=version_number  # Ahora es un número entero
    )
    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    
    
    # Generar archivos de navegación
    documents = db.query(Document).filter(Document.user_id == user_id).all()
    docs_data = [{"document_id": doc.document_id, "title": doc.title} for doc in documents]
    NavigationGenerator.generate_sidebar(docs_data, Config.UPLOAD_FOLDER)
    NavigationGenerator.generate_footer(Config.UPLOAD_FOLDER)
    
    return {
        "document_id": new_document.document_id,
        "title": new_document.title,
        "version": new_document.version,
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
        {"document_id": doc.document_id, "title": doc.title, "original_format": doc.original_format, "version": doc.version}
        for doc in documents
    ]
    
    return {"documents": documents_data}

@router.get("/versions/")
async def get_document_versions(
    title: str = Query(...),
    page: int = Query(1),
    limit: int = Query(10),
    user_id: int = Depends(get_user_from_token),
    db: Session = Depends(get_db)
):
    # Verificar usuario
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Buscar documentos que coincidan con el título
    documents = db.query(Document).filter(
        Document.user_id == user_id,
        Document.title.like(f"%{title}%")
    ).all()
    
    if not documents:
        return {"versions": [], "has_more": False}
    
    # Obtener los IDs de los documentos (igual que antes)
    document_ids = [doc.document_id for doc in documents]
    
    # Consultar versiones usando solo Document (cambia esta parte)
    skip = (page - 1) * limit
    versions_query = db.query(Document).filter(
        Document.document_id.in_(document_ids)
    ).order_by(Document.created_at.desc())
    
    # Contar total de versiones para determinar si hay más
    total_versions = versions_query.count()
    
    # Aplicar paginación (igual que antes)
    versions = versions_query.offset(skip).limit(limit + 1).all()
    
    # Determinar si hay más resultados (igual que antes)
    has_more = len(versions) > limit
    if has_more:
        versions = versions[:limit]
    
    # Obtener información (adaptado para usar Document directamente)
    result_versions = []
    for version in versions:
        result_versions.append({
            "version_id": version.document_id,  # Usamos document_id como version_id
            "document_id": version.document_id,
            "title": version.title,
            "version_number": version.version,  # Usamos version en lugar de version_number
            "created_at": version.created_at
        })
    
    return {"versions": result_versions, "has_more": has_more}

@router.delete("/versions/{document_id}/{version_number}")
async def delete_document_version(
    document_id: int,
    version_number: int,
    user_id: int = Depends(get_user_from_token),
    db: Session = Depends(get_db)
):
    # Verificar usuario
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Buscar y verificar el documento
    document = db.query(Document).filter(
        Document.document_id == document_id,
        Document.version == version_number,
        Document.user_id == user_id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=404,
            detail="Versión del documento no encontrada o no tienes permisos"
        )
    
    # Eliminar el documento directamente (ya no hay restricciones)
    db.delete(document)
    db.commit()
    
    return {
        "message": "Versión eliminada correctamente",
        "document_id": document_id,
        "version": version_number
    }

@router.get("/content/{document_id}")
async def get_document_content(
    document_id: int,
    user_id: int = Depends(get_user_from_token),
    db: Session = Depends(get_db)
):
    # Verificar usuario
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Buscar documento
    document = db.query(Document).filter(Document.document_id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    
    # Verificar que el usuario tenga acceso al documento
    if document.user_id != user_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a este documento")
    
    return {
        "document_id": document.document_id,
        "title": document.title,
        "version": document.version,
        "markdown_content": document.markdown_content
    }

@router.post("/improve/{document_id}")
async def improve_document(
    document_id: int,
    user_id: int = Depends(get_user_from_token),
    db: Session = Depends(get_db)
):
    # Verificar usuario
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Buscar documento
    document = db.query(Document).filter(Document.document_id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    
    # Verificar que el usuario tenga acceso al documento
    if document.user_id != user_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a este documento")
    
    # Obtener contenido Markdown
    markdown_content = document.markdown_content
    
    # Manejar imágenes en base64
    try:
        import re
        import uuid
        
        # Patrones para identificar imágenes en Markdown, incluyendo imágenes en base64
        image_pattern = r'!\[([^\]]*)\]\((data:image\/[^;]+;base64,[^)]+)\)'
        
        # Diccionario para almacenar imágenes extraídas
        extracted_images = {}
        
        # Función para reemplazar imágenes con marcadores
        def extract_image(match):
            alt_text = match.group(1)
            image_data = match.group(2)
            image_id = str(uuid.uuid4())
            extracted_images[image_id] = {
                'alt_text': alt_text,
                'data': image_data
            }
            return f'![{alt_text}]({{{image_id}}})'
        
        # Extraer imágenes del contenido Markdown
        markdown_without_images = re.sub(image_pattern, extract_image, markdown_content)
        
        # Mejorar el contenido con Azure AI
        from azure.ai.inference import ChatCompletionsClient
        from azure.ai.inference.models import SystemMessage, UserMessage
        from azure.core.credentials import AzureKeyCredential
        
        endpoint = "https://elvle-ma7lv0mp-eastus2.services.ai.azure.com/models"
        model_name = "DeepSeek-R1"
        
        client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential("5W72u700MMJdrQ2aHhUxbD1iN5G86vkOVkfTcQylM1XwrhCMt3NSJQQJ99BEACHYHv6XJ3w3AAAAACOGUZnR"),
        )
        
        system_prompt = """Eres un asistente especializado en mejorar documentos Markdown. 
        
        INSTRUCCIONES IMPORTANTES:
        1. Corrige errores ortográficos y gramaticales sin cambiar las palabras originales.
        2. Mejora el formato de títulos, subtítulos, listas y tablas.
        3. No cambies la spalabras que tiene el documento, solo puedes corregirlas mas no resumir nada.
        4. MANTÉN TODOS LOS MARCADORES DE IMÁGENES tal como están, NO los modifiques.
        5. Los marcadores de imágenes tienen el formato ![texto_alternativo]({uuid}) - NO CAMBIES estos marcadores.
        6. DEVUELVE ÚNICAMENTE EL CÓDIGO MARKDOWN MEJORADO.
        7. NO incluyas explicaciones, comentarios, introducciones o conclusiones.
        8. NO añadas marcadores como "```markdown" o "```" alrededor del contenido.
        9. NO incluyas frases como "Aquí está el documento mejorado:" o similares.
        10. El output debe ser EXCLUSIVAMENTE el documento Markdown mejorado y nada más.
        
        Tu respuesta debe contener solamente el contenido Markdown mejorado, sin ningún otro texto."""
        
        response = client.complete(
            messages=[
                SystemMessage(content=system_prompt),
                UserMessage(content=f"Mejora este documento Markdown:\n\n{markdown_without_images}")
            ],
            max_tokens=10000,
            model=model_name
        )
        
        improved_content = response.choices[0].message.content
        improved_content = re.sub(r'<think>.*?</think>', '', improved_content, flags=re.DOTALL)
        improved_content = improved_content.strip()
        
        # Reinsertar las imágenes en el contenido mejorado
        def reinsert_image(match):
            image_id = match.group(2)  # Cambiado de group(1) a group(2) para capturar el UUID correctamente
            if image_id in extracted_images:
                img = extracted_images[image_id]
                return f'![{img["alt_text"]}]({img["data"]})'
            return match.group(0)
        
        # Patrón para buscar los marcadores de imagen temporales
        placeholder_pattern = r'!\[([^\]]*)\]\(\{([^}]+)\}\)'
        improved_content_with_images = re.sub(placeholder_pattern, reinsert_image, improved_content)
        
        new_version = document.version + 1
        
        new_document = Document(
            user_id=user_id,
            title=f"{document.title} (Mejorado)",
            original_format="md",
            markdown_content=improved_content_with_images,
            version=new_version
        )
        
        db.add(new_document)
        db.commit()
        db.refresh(new_document)
        
        return {
            "document_id": new_document.document_id,
            "title": new_document.title,
            "version": new_document.version,
            "markdown_content": improved_content_with_images
        }
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"Error al mejorar el documento: {str(e)}\n{error_details}")