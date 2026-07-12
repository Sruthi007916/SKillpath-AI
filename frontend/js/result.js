document.addEventListener("DOMContentLoaded", () => {

    const result = JSON.parse(
        localStorage.getItem("assessmentResult")
    );

    if (!result) {

        window.location.href = "assessment.html";
        return;
    }

    const scoreElement = document.getElementById("userScore");
    const careerElement = document.getElementById("careerPath");
    const skillsElement = document.getElementById("skillRecommendations");
    const roadmapElement = document.getElementById("learningRoadmap");

    scoreElement.textContent = result.score;
    careerElement.textContent = result.recommended_path;

    let skills = [];
    let roadmap = [];

    switch (result.recommended_path) {

        case "Data Scientist":

            skills = [
                "Python",
                "Pandas",
                "NumPy",
                "Machine Learning",
                "SQL",
                "Data Visualization"
            ];

            roadmap = [
                "Complete Python Fundamentals",
                "Learn Data Analysis",
                "Study Machine Learning",
                "Build Real-world Projects",
                "Earn Data Science Certification"
            ];

            break;

        case "Backend Developer":

            skills = [
                "Python",
                "Flask",
                "REST API",
                "MySQL",
                "Git",
                "Docker"
            ];

            roadmap = [
                "Learn Python",
                "Build APIs using Flask",
                "Practice Database Design",
                "Create Full Stack Projects",
                "Deploy Applications"
            ];

            break;

        case "Frontend Developer":

            skills = [
                "HTML",
                "CSS",
                "JavaScript",
                "Bootstrap",
                "React"
            ];

            roadmap = [
                "Master HTML & CSS",
                "Learn JavaScript",
                "Build Responsive Websites",
                "Learn React",
                "Create Portfolio Projects"
            ];

            break;

        default:

            skills = [
                "Manual Testing",
                "Automation Testing",
                "Selenium",
                "SQL",
                "Bug Tracking"
            ];

            roadmap = [
                "Learn Testing Basics",
                "Practice Test Cases",
                "Study Selenium",
                "Learn SQL",
                "Work on Testing Projects"
            ];
    }

    skillsElement.innerHTML = "";

    skills.forEach(skill => {

        skillsElement.innerHTML += `
            <span class="badge bg-info text-dark m-2 p-2">
                ${skill}
            </span>
        `;
    });

    roadmapElement.innerHTML = "";

    roadmap.forEach(step => {

        roadmapElement.innerHTML += `
            <li class="list-group-item bg-transparent text-white border-secondary">
                ${step}
            </li>
        `;
    });

});