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
                    li.className = "list-group-item";
                    
                    // Crear el enlace sin subrayado
                    const link = document.createElement("a");
                    link.href = `/api/documents/download/${doc.document_id}`;
                    link.target = "_blank";
                    link.textContent = doc.title;
                    link.style.textDecoration = "none"; // Elimina el subrayado
                    link.style.color = "#0d6efd"; // Color negro
                    link.style.fontWeight = "normal"; // Peso normal (o usa "bold" si prefieres negrita)
                    
                    // Crear el texto de versión
                    const versionSpan = document.createElement("span");
                    versionSpan.textContent = ` Version ${doc.version}`;
                    versionSpan.style.marginLeft = "8px";
                    versionSpan.style.color = "#666"; // Gris oscuro
                    
                    // Agregar ambos elementos al li
                    li.appendChild(link);
                    li.appendChild(versionSpan);
                    
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
