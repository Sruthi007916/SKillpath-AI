document.addEventListener("DOMContentLoaded", () => {

    const assessmentForm = document.getElementById("assessmentForm");

    if (!assessmentForm) return;

    assessmentForm.addEventListener("submit", async (e) => {

        e.preventDefault();

        let score = 0;

        const answers = document.querySelectorAll(
            'input[type="radio"]:checked'
        );

        answers.forEach(answer => {
            score += parseInt(answer.value);
        });

        const result = await submitAssessment(score);

        if (result.success) {

            localStorage.setItem(
                "assessmentResult",
                JSON.stringify(result.result)
            );
            window.location.href = "result.html";

        } else {

            alert("Failed to submit assessment.");
        }

    });

});