/* ============================================
   api.js — shared API functions
   used by login.js, register.js, dashboard, etc.
   ============================================ */

const API_BASE = "http://127.0.0.1:5000";

/* ---------- REGISTER ---------- */
async function registerUser({ name, email, password }) {
    try {
        const res = await fetch(`${API_BASE}/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, email, password })
        });
        const data = await res.json();

        if (!res.ok) {
            return { success: false, message: data.message || "Registration failed" };
        }
        return { success: true, message: data.message };

    } catch (err) {
        console.error(err);
        return { success: false, message: "Could not connect to server. Is Flask running?" };
    }
}

/* ---------- LOGIN ---------- */
async function loginUser({ email, password }) {
    try {
        const res = await fetch(`${API_BASE}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });
        const data = await res.json();

        if (!res.ok) {
            return { success: false, message: data.message || "Login failed" };
        }

        // Build a user object matching what login.js expects
        return {
            success: true,
            user: {
                id: data.user_id,
                name: data.name,
                email: email,
                has_profile: data.has_profile
            }
        };

    } catch (err) {
        console.error(err);
        return { success: false, message: "Could not connect to server. Is Flask running?" };
    }
}

/* ---------- GENERIC GET ---------- */
async function apiGet(endpoint) {
    const res = await fetch(`${API_BASE}${endpoint}`);
    const data = await res.json();
    if (!res.ok) throw new Error(data.message || "Request failed");
    return data;
}

/* ---------- GENERIC POST ---------- */
async function apiPost(endpoint, body) {
    const res = await fetch(`${API_BASE}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.message || "Request failed");
    return data;
}