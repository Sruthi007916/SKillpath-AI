document.addEventListener("DOMContentLoaded", () => {

    const result = JSON.parse(
        localStorage.getItem("assessmentResult")
    );

    const profile = JSON.parse(
        localStorage.getItem("profileData")
    );

    if (!result || !profile) {
        return;
    }

    const careerPath = document.getElementById("dashboardCareer");
    const score = document.getElementById("dashboardScore");
    const skills = document.getElementById("dashboardSkills");

    if (careerPath) {
        careerPath.textContent = result.recommended_path;
    }

    if (score) {
        score.textContent = result.score + "%";
    }

    if (skills) {

        const skillList = profile.skills.split(",");

        skills.innerHTML = "";

        skillList.forEach(skill => {

            skills.innerHTML += `
                <span class="badge bg-info text-dark m-2 p-2">
                    ${skill.trim()}
                </span>
            `;
        });
    }

});