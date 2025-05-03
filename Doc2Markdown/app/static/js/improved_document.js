document.addEventListener("DOMContentLoaded", () => {
    checkAuth(); // Asegúrate de que el usuario esté autenticado
    
    // Obtener el ID del documento de la URL
    const url = window.location.pathname;
    const documentId = url.split('/').pop();
    
    // Obtener y mostrar el documento mejorado
    loadImprovedDocument(documentId);
    
    // Configurar el botón de descarga
    const downloadBtn = document.getElementById("downloadBtn");
    downloadBtn.addEventListener("click", () => {
        downloadImprovedDocument(documentId);
    });
});

async function loadImprovedDocument(documentId) {
    try {
        const response = await fetch(`/api/documents/content/${documentId}`, {
            method: "GET",
            headers: { 
                "Authorization": `Bearer ${localStorage.getItem("access_token")}` 
            }
        });
        
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || "Error al obtener el documento mejorado");
        }
        
        const data = await response.json();
        
        // Actualizar el título
        document.getElementById('documentTitle').textContent = `${data.title} (Versión ${data.version})`;
        
        // Configuración de marked.js para manejar correctamente imágenes en base64
        marked.setOptions({
            breaks: true,
            gfm: true,
            headerIds: true,
            mangle: false
        });
        
        // Convertir Markdown a HTML usando marked.js y mostrarlo
        const previewContent = document.getElementById('previewContent');
        previewContent.innerHTML = marked.parse(data.markdown_content);
        
        // Añadir CSS para manejar imágenes grandes
        const style = document.createElement('style');
        style.textContent = `
            #previewContent img {
                max-width: 100%;
                height: auto;
                margin: 10px 0;
            }
        `;
        document.head.appendChild(style);
        
    } catch (error) {
        console.error("Error:", error);
        alert("Ocurrió un error: " + error.message);
    }
}

async function downloadImprovedDocument(documentId) {
    try {
        const response = await fetch(`/api/documents/content/${documentId}`, {
            method: "GET",
            headers: { 
                "Authorization": `Bearer ${localStorage.getItem("access_token")}` 
            }
        });
        
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || "Error al obtener el documento mejorado");
        }
        
        const data = await response.json();
        
        // Crear un archivo Blob con el contenido Markdown
        const blob = new Blob([data.markdown_content], { type: 'text/markdown' });
        const url = window.URL.createObjectURL(blob);
        
        // Crear un enlace para descargar y hacer clic en él
        const a = document.createElement('a');
        a.href = url;
        a.download = `${data.title}_mejorado.md`;
        document.body.appendChild(a);
        a.click();
        
        // Limpiar
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
    } catch (error) {
        console.error("Error:", error);
        alert("Ocurrió un error: " + error.message);
    }
}