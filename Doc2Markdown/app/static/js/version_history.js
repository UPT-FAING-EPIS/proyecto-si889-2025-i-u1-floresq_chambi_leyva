document.addEventListener("DOMContentLoaded", () => {
    checkAuth(); // Asegúrate de que el usuario esté autenticado
    
    const searchBtn = document.getElementById("searchBtn");
    const loadMoreBtn = document.getElementById("loadMoreBtn");
    
    let currentPage = 1;
    let currentSearch = "";
    
    searchBtn.addEventListener("click", () => {
        currentPage = 1;
        currentSearch = document.getElementById("documentSearch").value.trim();
        searchVersions(currentSearch, currentPage);
    });
    
    loadMoreBtn.addEventListener("click", (e) => {
        e.preventDefault();
        currentPage++;
        searchVersions(currentSearch, currentPage);
    });
});

async function searchVersions(documentTitle, page) {
    const versionsList = document.getElementById("versionsList");
    const loadMoreContainer = document.getElementById("loadMoreContainer");
    
    if (page === 1) {
        versionsList.innerHTML = ""; // Limpiar solo en la primera página
    }
    
    if (!documentTitle) {
        versionsList.innerHTML = "<li class='list-group-item'>Por favor, introduce un nombre de documento.</li>";
        loadMoreContainer.style.display = "none";
        return;
    }
    
    try {
        const response = await fetch(`/api/documents/versions/?title=${encodeURIComponent(documentTitle)}&page=${page}&limit=10`, {
            method: "GET",
            headers: { 
                "Authorization": `Bearer ${localStorage.getItem("access_token")}` 
            }
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || "Error al buscar versiones");
        }
        
        if (data.versions.length === 0 && page === 1) {
            versionsList.innerHTML = "<li class='list-group-item'>No se encontraron versiones para este documento.</li>";
            loadMoreContainer.style.display = "none";
            return;
        }
        
        data.versions.forEach(version => {
            const li = document.createElement("li");
            li.className = "list-group-item d-flex justify-content-between align-items-center";
            
            // Enlace de descarga para el título
            const downloadLink = document.createElement("a");
            downloadLink.href = `/api/documents/download/${version.document_id}`;
            downloadLink.target = "_blank";
            downloadLink.style.textDecoration = "none";
            downloadLink.style.color = "#0d6efd"; // Azul Bootstrap para enlaces
            downloadLink.style.marginRight = "8px";
            downloadLink.textContent = version.title;
            
            // Texto normal negro para la versión
            const versionSpan = document.createElement("span");
            versionSpan.style.color = "#000"; // Texto negro
            versionSpan.style.marginRight = "8px";
            versionSpan.textContent = `Versión ${version.version_number}`;
            
            // Fecha en gris
            const dateSpan = document.createElement("small");
            dateSpan.className = "text-muted";
            dateSpan.textContent = new Date(version.created_at).toLocaleString();
            
            // Botón de eliminar
            const deleteBtn = document.createElement("a");
            deleteBtn.href = "#";
            deleteBtn.className = "text-danger";
            deleteBtn.textContent = "Eliminar";
            deleteBtn.onclick = (e) => {
                e.preventDefault();
                deleteVersion(version.document_id, version.version_number);
            };
            
            // Agregar elementos al li
            li.appendChild(downloadLink);
            li.appendChild(versionSpan);
            li.appendChild(dateSpan);
            li.appendChild(deleteBtn);
            
            versionsList.appendChild(li);
        });
        
        // Mostrar u ocultar el botón "Ver más" según si hay más resultados
        loadMoreContainer.style.display = data.has_more ? "block" : "none";
        
    } catch (error) {
        console.error("Error:", error);
        alert("Ocurrió un error: " + error.message);
    }
}

async function deleteVersion(documentId, versionNumber) {
    if (!confirm("¿Estás seguro de que deseas eliminar esta versión?")) {
        return;
    }
    
    try {
        const response = await fetch(`/api/documents/versions/${documentId}/${versionNumber}`, {
            method: "DELETE",
            headers: { 
                "Authorization": `Bearer ${localStorage.getItem("access_token")}` 
            }
        });
        
        if (response.ok) {
            // Recargar la lista o eliminar el elemento visualmente
            currentPage = 1;
            searchVersions(currentSearch, currentPage);
            
            showAlert("Versión eliminada correctamente", "success");
        } else {
            const data = await response.json();
            throw new Error(data.detail || "Error al eliminar la versión");
        }
    } catch (error) {
        console.error("Error:", error);
        showAlert("Ocurrió un error: " + error.message, "danger");
    }
}