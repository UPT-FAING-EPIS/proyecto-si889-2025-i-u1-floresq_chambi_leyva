document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("loginForm");
    const registerForm = document.getElementById("registerForm");

    if (loginForm) {
        loginForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;

            const response = await fetch("/api/users/token", {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: new URLSearchParams({ username, password })
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem("access_token", data.access_token);
                window.location.href = "/document_conversion";
            } else {
                alert("Usuario o contraseña incorrectos.");
            }
        });
    }

    if (registerForm) {
        registerForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const username = document.getElementById("regUsername").value;
            const email = document.getElementById("regEmail").value;
            const password = document.getElementById("regPassword").value;

            const response = await fetch("/api/users/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, email, password })
            });

            if (response.ok) {
                alert("Usuario registrado. Ahora inicia sesión.");
                window.location.href = "/login";
            } else {
                alert("Error al registrar usuario.");
            }
        });
    }
});
