import os
from pathlib import Path
from typing import List, Dict
from datetime import datetime

class NavigationGenerator:
    @staticmethod
    def generate_sidebar(documents: List[Dict], output_path: str) -> str:
        """
        Genera un archivo _Sidebar.md con enlaces a los documentos convertidos.
        
        Args:
            documents: Lista de diccionarios con información de documentos
            output_path: Ruta donde se guardará el archivo
            
        Returns:
            str: Ruta del archivo generado
        """
        sidebar_content = "# Navegación\n\n"
        sidebar_content += "## Documentos\n\n"
        
        for doc in documents:
            doc_title = doc.get('title', 'Documento sin título')
            doc_id = doc.get('document_id', '')
            sidebar_content += f"- [{doc_title}](document_{doc_id}.md)\n"
        
        sidebar_content += "\n---\n"
        sidebar_content += f"\n> Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        sidebar_path = os.path.join(output_path, "_Sidebar.md")
        with open(sidebar_path, 'w', encoding='utf-8') as f:
            f.write(sidebar_content)
        
        return sidebar_path

    @staticmethod
    def generate_footer(output_path: str) -> str:
        """
        Genera un archivo _Footer.md con información básica.
        
        Args:
            output_path: Ruta donde se guardará el archivo
            
        Returns:
            str: Ruta del archivo generado
        """
        footer_content = "---\n\n"
        footer_content += "© 2023 Doc2Markdown | [Acerca de](#) | [Contacto](#)\n"
        footer_content += f"\n> Generado el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        footer_path = os.path.join(output_path, "_Footer.md")
        with open(footer_path, 'w', encoding='utf-8') as f:
            f.write(footer_content)
        
        return footer_path