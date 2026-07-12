document.addEventListener("DOMContentLoaded", () => {

    const loginForm = document.getElementById("loginForm");

    if (!loginForm) return;

    loginForm.addEventListener("submit", async (e) => {

        e.preventDefault();

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        const result = await loginUser({
            email,
            password
        });

        if (result.success) {

            localStorage.setItem(
                "currentUser",
                JSON.stringify(result.user)
            );

            window.location.href = "dashboard.html";

        } else {

            alert(result.message);
        }
    });
});