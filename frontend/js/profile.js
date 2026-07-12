document.getElementById("profileForm").addEventListener("submit", function (e) {

    e.preventDefault();

    const user = {

        name: document.getElementById("name").value,

        education: document.getElementById("education").value,

        department: document.getElementById("department").value,

        goal: document.getElementById("goal").value,

        skills: document.getElementById("skills").value
            .split(",")
            .map(skill => skill.trim()),

        interests: document.getElementById("interests").value
            .split(",")
            .map(item => item.trim()),

        language: document.getElementById("language").value,

        pace: document.getElementById("pace").value
    };

    localStorage.setItem(
        "userProfile",
        JSON.stringify(user)
    );

    window.location.href = "dashboard.html";

});