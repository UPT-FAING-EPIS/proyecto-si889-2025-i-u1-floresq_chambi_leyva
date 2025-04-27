// Función para verificar si el usuario está autenticado
function checkAuth() {
    const token = localStorage.getItem("access_token");
    const loginBtn = document.getElementById("loginBtn");
    const registerBtn = document.getElementById("registerBtn");
    const logoutBtn = document.getElementById("logoutBtn");
    const userName = document.getElementById("userName");

    if (token) {
        // Si el token existe, el usuario está logueado
        loginBtn.classList.add("d-none");  // Ocultar el botón de login
        registerBtn.classList.add("d-none"); // Ocultar el botón de registro
        logoutBtn.classList.remove("d-none");  // Mostrar el botón de logout
        userName.classList.remove("d-none"); // Mostrar el nombre de usuario
        userName.innerText = "Usuario logueado"; // Cambiar el texto
    } else {
        // Si no hay token, muestra los botones de Login y Registrarse
        loginBtn.classList.remove("d-none");
        registerBtn.classList.remove("d-none");
        logoutBtn.classList.add("d-none");
        userName.classList.add("d-none");
    }
}

document.addEventListener("DOMContentLoaded", () => {
    // Llamamos a checkAuth para manejar el estado de los botones
    checkAuth();

    // Lógica para cerrar sesión
    document.getElementById("logoutBtn").addEventListener("click", () => {
        // Eliminar el token de acceso
        localStorage.removeItem("access_token");

        // Redirigir al usuario al login
        window.location.href = "/login";
    });
});
