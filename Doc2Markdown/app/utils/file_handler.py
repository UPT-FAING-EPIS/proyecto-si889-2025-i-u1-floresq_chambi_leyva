import os
import uuid
import shutil
from pathlib import Path
from typing import Optional, Tuple
from fastapi import UploadFile
from werkzeug.utils import secure_filename
from config.config import Config

class FileHandler:
    @staticmethod
    def allowed_file(filename: str) -> bool:
        """Verifica si la extensión del archivo está permitida"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

    @staticmethod
    async def save_uploaded_file(file: UploadFile) -> Optional[Tuple[str, str]]:
        """
        Guarda un archivo subido en el sistema de archivos.
        
        Args:
            file: Archivo subido desde el formulario
            
        Returns:
            Tuple: (nombre seguro del archivo, ruta completa) o None si falla
        """
        if file and FileHandler.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Agregar un UUID para evitar colisiones
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            filepath = os.path.join(Config.UPLOAD_FOLDER, unique_filename)

            # Guardar el archivo usando shutil
            with open(filepath, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            return unique_filename, filepath
        return None

    @staticmethod
    def get_file_extension(filename: str) -> str:
        """Obtiene la extensión del archivo"""
        return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

    @staticmethod
    def clean_upload_folder():
        """Limpia la carpeta de uploads"""
        for filename in os.listdir(Config.UPLOAD_FOLDER):
            file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
