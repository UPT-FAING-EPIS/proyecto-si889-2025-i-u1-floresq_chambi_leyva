import os
import tempfile
from typing import Optional
from pathlib import Path
from datetime import datetime
import pdfplumber
import mammoth
import markdown
from bs4 import BeautifulSoup
import html2text
from config.config import Config

class DocumentConverter:
    @staticmethod
    def convert_to_markdown(file_path: str, original_format: str) -> Optional[str]:
        """
        Convierte un documento a formato Markdown.
        
        Args:
            file_path: Ruta al archivo a convertir
            original_format: Formato original del documento (doc, docx, pdf, html, txt)
            
        Returns:
            str: Contenido en formato Markdown o None si falla la conversión
        """
        try:
            if original_format.lower() in ['doc', 'docx']:
                return DocumentConverter._convert_word_to_markdown(file_path)
            elif original_format.lower() == 'pdf':
                return DocumentConverter._convert_pdf_to_markdown(file_path)
            elif original_format.lower() == 'html':
                return DocumentConverter._convert_html_to_markdown(file_path)
            elif original_format.lower() == 'txt':
                return DocumentConverter._convert_txt_to_markdown(file_path)
            else:
                return None
        except Exception as e:
            print(f"Error during conversion: {str(e)}")
            return None

    @staticmethod
    def _convert_word_to_markdown(file_path: str) -> str:
        """Convierte archivos Word (docx) a Markdown"""
        try:
            with open(file_path, "rb") as docx_file:
                result = mammoth.convert_to_markdown(docx_file)
                # Limpiar posibles barras invertidas o caracteres de LaTeX innecesarios
                markdown_content = result.value.replace("\\", "")
                return markdown_content.strip()
        except Exception as e:
            print(f"Error converting Word to Markdown: {str(e)}")
            return ""

    @staticmethod
    def _convert_pdf_to_markdown(file_path: str) -> str:
        """Convierte archivos PDF a Markdown"""
        try:
            markdown_content = []
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        # Limpiar texto extraído de PDF, eliminando caracteres no deseados
                        cleaned_text = text.replace("\n", " ").replace("\r", "")
                        markdown_content.append(cleaned_text.strip())
            return "\n\n".join(markdown_content).strip()
        except Exception as e:
            print(f"Error converting PDF to Markdown: {str(e)}")
            return ""

    @staticmethod
    def _convert_html_to_markdown(file_path: str) -> str:
        """Convierte archivos HTML a Markdown"""
        try:
            with open(file_path, 'r', encoding='utf-8') as html_file:
                soup = BeautifulSoup(html_file, 'html.parser')
                # Eliminar scripts y estilos
                for script in soup(["script", "style"]):
                    script.decompose()
                text = soup.get_text()
                # Convertir HTML a Markdown de manera más confiable usando html2text
                markdown_content = html2text.html2text(text)
                return markdown_content.strip()
        except Exception as e:
            print(f"Error converting HTML to Markdown: {str(e)}")
            return ""

    @staticmethod
    def _convert_txt_to_markdown(file_path: str) -> str:
        """Convierte archivos de texto plano a Markdown (básico)"""
        try:
            with open(file_path, 'r', encoding='utf-8') as txt_file:
                content = txt_file.read()
                # Convertir saltos de línea dobles a párrafos de Markdown
                return content.replace('\n\n', '\n\n').strip()
        except Exception as e:
            print(f"Error converting TXT to Markdown: {str(e)}")
            return ""

    @staticmethod
    def convert_and_save(file_path: str, original_format: str, output_dir: str) -> Optional[str]:
        """
        Convierte el archivo a Markdown y lo guarda en un archivo en el directorio de salida.

        Args:
            file_path: Ruta al archivo a convertir.
            original_format: Formato original del archivo (docx, pdf, html, txt).
            output_dir: Directorio donde se guardará el archivo Markdown.

        Returns:
            str: Ruta al archivo Markdown generado o None si falla la conversión.
        """
        try:
            # Convierte el archivo al formato Markdown
            markdown_content = DocumentConverter.convert_to_markdown(file_path, original_format)
            if not markdown_content:
                return None
            
            # Asegurarse de que el directorio de salida exista
            os.makedirs(output_dir, exist_ok=True)
            
            # Generar nombre para el archivo de salida
            base_filename = Path(file_path).stem
            markdown_file_path = os.path.join(output_dir, f"{base_filename}.md")

            # Guardar el contenido en el archivo Markdown
            with open(markdown_file_path, 'w', encoding='utf-8') as md_file:
                md_file.write(markdown_content)
            
            return markdown_file_path
        except Exception as e:
            print(f"Error during conversion and saving: {str(e)}")
            return None
