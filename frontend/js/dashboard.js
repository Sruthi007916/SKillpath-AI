/* ============================================
   dashboard-init.js
   Reads the logged-in user from localStorage
   (key: "currentUser") and loads dashboard data
   ============================================ */

const API_BASE = "http://127.0.0.1:5000";

window.addEventListener("DOMContentLoaded", async () => {

    // Read the single currentUser object saved by login.js
    const stored = localStorage.getItem("currentUser");

    if (!stored) {
        window.location.href = "login.html";
        return;
    }

    const currentUser = JSON.parse(stored);
    const userId    = currentUser.id;
    const userName  = currentUser.name || "Learner";
    const userEmail = currentUser.email || "";

    fillUserInfo(userName, userEmail);

    try {
        const res  = await fetch(`${API_BASE}/dashboard/${userId}`);
        const data = await res.json();
        if (!res.ok) throw new Error(data.message || "Failed to load dashboard");
        fillDashboard(data);
    } catch (err) {
        console.error(err);
        showError("Could not load dashboard data. Make sure the backend is running.");
    } finally {
        const overlay = document.getElementById("loadingOverlay");
        if (overlay) overlay.style.display = "none";
    }
});

function fillUserInfo(name, email) {
    const first   = name.split(" ")[0];
    const initial = name.charAt(0).toUpperCase();
    setText("greeting", `Welcome back, ${first}! 👋`);
    setText("sidebar-name", name);
    setText("sidebar-email", email);
    setText("sidebar-avatar", initial);
}

function setText(id, val) {
    const el = document.getElementById(id);
    if (el) el.textContent = val;
}

function showError(msg) {
    const el = document.getElementById("dash-error");
    if (el) { el.textContent = msg; el.style.display = "block"; }
}

/* fillDashboard(d) — keep your existing version from dashboard.html
   that fills stat cards, charts, recommendations, etc. */