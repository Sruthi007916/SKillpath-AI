document.addEventListener("DOMContentLoaded", () => {

    const registerForm = document.getElementById("registerForm");

    if (!registerForm) return;

    registerForm.addEventListener("submit", async (e) => {

        e.preventDefault();

        const name = document.getElementById("name").value.trim();
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value.trim();

        const result = await registerUser({
            name,
            email,
            password
        });

        if (result.success) {

            alert("Registration successful!");

            window.location.href = "login.html";

        } else {

            alert(result.message);
        }
    });

});