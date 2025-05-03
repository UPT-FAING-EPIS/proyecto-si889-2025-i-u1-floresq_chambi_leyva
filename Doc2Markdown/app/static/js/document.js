document.addEventListener("DOMContentLoaded", () => {
    checkAuth();
    fetchDocuments();

    const uploadForm = document.getElementById("uploadForm");
    uploadForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const title = document.getElementById("title").value;
        const fileInput = document.getElementById("fileInput").files[0];

        const formData = new FormData();
        formData.append("file", fileInput);
        formData.append("title", title);
        formData.append("user_id", 1); // Ajustar el user_id (puedes almacenarlo en localStorage también)

        const response = await fetch("/api/documents/upload/", {
            method: "POST",
            headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` },
            body: formData
        });

        if (response.ok) {
            alert("Documento subido correctamente.");
            fetchDocuments();
        } else {
            alert("Error al subir el documento.");
        }
    });
});

async function fetchDocuments() {
    const list = document.getElementById("documentList");
    list.innerHTML = ""; // Limpiar la lista antes de agregar nuevos documentos

    const userId = 1; // Obtener el user_id adecuado

    try {
        const response = await fetch(`/api/documents/list/?user_id=${userId}`, {
            method: "GET",
            headers: { 
                "Authorization": `Bearer ${localStorage.getItem("access_token")}` 
            }
        });

        if (response.ok) {
            const data = await response.json();
            const documents = data.documents;

            if (documents.length === 0) {
                const li = document.createElement("li");
                li.className = "list-group-item";
                li.textContent = "No tienes documentos.";
                list.appendChild(li);
            } else {
                documents.forEach(doc => {
                    const li = document.createElement("li");
                    li.className = "list-group-item d-flex justify-content-between align-items-center";

                    // Crear div para el título y la versión
                    const infoDiv = document.createElement("div");
                    
                    // Crear el enlace
                    const link = document.createElement("a");
                    link.href = `/api/documents/download/${doc.document_id}`;
                    link.target = "_blank";
                    link.textContent = doc.title;
                    link.style.textDecoration = "none";
                    link.style.color = "#0d6efd";
                    link.style.fontWeight = "normal";

                    // Crear el texto de versión
                    const versionSpan = document.createElement("span");
                    versionSpan.textContent = ` Version ${doc.version}`;
                    versionSpan.style.marginLeft = "8px";
                    versionSpan.style.color = "#666";

                    // Agregar título y versión al div info
                    infoDiv.appendChild(link);
                    infoDiv.appendChild(versionSpan);
                    
                    // Div para botones
                    const buttonsDiv = document.createElement("div");
                    
                    // Botón para previsualizar (puedes añadirlo si lo necesitas)
                    const previewBtn = document.createElement("button");
                    previewBtn.className = "btn btn-sm btn-outline-primary me-2";
                    previewBtn.textContent = "Previsualizar";
                    previewBtn.onclick = () => {
                        previewDocument(doc.document_id);
                    };
                    
                    // Nuevo botón para mejorar
                    const improveBtn = document.createElement("button");
                    improveBtn.className = "btn btn-sm btn-outline-success";
                    improveBtn.textContent = "Mejorar";
                    improveBtn.onclick = () => {
                        improveDocument(doc.document_id);
                    };
                    
                    // Añadir botones al div de botones
                    buttonsDiv.appendChild(previewBtn);
                    buttonsDiv.appendChild(improveBtn);

                    // Agregar ambos divs al li
                    li.appendChild(infoDiv);
                    li.appendChild(buttonsDiv);

                    list.appendChild(li);
                });
            }
        } else {
            alert("Error al obtener documentos.");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Ocurrió un error al obtener los documentos.");
    }
}

// Función para mejorar un documento
async function improveDocument(documentId) {
    try {
        // Mostrar mensaje de carga
        const loadingModal = document.createElement("div");
        loadingModal.style.position = "fixed";
        loadingModal.style.top = "0";
        loadingModal.style.left = "0";
        loadingModal.style.width = "100%";
        loadingModal.style.height = "100%";
        loadingModal.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
        loadingModal.style.display = "flex";
        loadingModal.style.justifyContent = "center";
        loadingModal.style.alignItems = "center";
        loadingModal.style.zIndex = "1000";
        
        const loadingContent = document.createElement("div");
        loadingContent.style.backgroundColor = "white";
        loadingContent.style.padding = "20px";
        loadingContent.style.borderRadius = "5px";
        loadingContent.style.textAlign = "center";
        
        const spinner = document.createElement("div");
        spinner.className = "spinner-border text-primary";
        spinner.setAttribute("role", "status");
        
        const loadingText = document.createElement("div");
        loadingText.textContent = "Mejorando documento... Esto puede tardar unos momentos.";
        loadingText.style.marginTop = "10px";
        
        loadingContent.appendChild(spinner);
        loadingContent.appendChild(loadingText);
        loadingModal.appendChild(loadingContent);
        document.body.appendChild(loadingModal);
        
        // Llamar a la API para mejorar el documento
        const response = await fetch(`/api/documents/improve/${documentId}`, {
            method: "POST",
            headers: { 
                "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
                "Content-Type": "application/json" 
            }
        });
        
        // Eliminar modal de carga
        document.body.removeChild(loadingModal);
        
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || "Error al mejorar el documento");
        }
        
        const data = await response.json();
        
        // Redirigir a la página de documento mejorado
        window.location.href = `/improved_document/${data.document_id}`;
        
    } catch (error) {
        console.error("Error:", error);
        alert("Ocurrió un error: " + error.message);
    }
}

// Función para previsualizar documento (añadida para completitud)
async function previewDocument(documentId) {
    try {
        const response = await fetch(`/api/documents/content/${documentId}`, {
            method: "GET",
            headers: { 
                "Authorization": `Bearer ${localStorage.getItem("access_token")}` 
            }
        });
        
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || "Error al obtener el contenido del documento");
        }
        
        const data = await response.json();
        
        // Mostrar modal con previsualización (implementa esta funcionalidad según tus necesidades)
        // Aquí puedes usar un modal existente o crear uno nuevo
        
    } catch (error) {
        console.error("Error:", error);
        alert("Ocurrió un error: " + error.message);
    }
}