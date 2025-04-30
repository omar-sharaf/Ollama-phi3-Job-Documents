async function generateCoverLetter() {
    const resume = document.getElementById("resume").value;
    const jobDescription = document.getElementById("job-description").value;

    try {
        const response = await fetch("/generate_cover_letter", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                resume_text: resume,
                job_description: jobDescription,
            }),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        document.getElementById("output").textContent = data.cover_letter;
    } catch (error) {
        console.error('Error:', error);
        document.getElementById("output").textContent = 'Error generating cover letter. Please try again.';
    }
}

async function resizeResume() {
    const resume = document.getElementById("resume").value;
    const pageLength = document.getElementById("page-length").value;

    try {
        const response = await fetch("/resize_resume", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                resume_text: resume,
                target_page_length: pageLength,
            }),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        document.getElementById("output").textContent = data.resume_resizing_guidance;
    } catch (error) {
        console.error('Error:', error);
        document.getElementById("output").textContent = 'Error getting resume resizing guidance. Please try again.';
    }
}