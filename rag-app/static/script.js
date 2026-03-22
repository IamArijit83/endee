async function uploadFile() {
    const fileInput = document.getElementById("fileInput");
    const status = document.getElementById("uploadStatus");

    if (!fileInput.files.length) {
        alert("Please select a file first");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
        const res = await fetch("http://127.0.0.1:8000/upload", {
            method: "POST",
            body: formData
        });

        const data = await res.json();
        status.innerText = "Uploaded! Chunks: " + data.chunks;

    } catch (err) {
        console.error(err);
        alert("Upload failed");
    }
}

async function askQuestion() {
    const query = document.getElementById("queryInput").value;
    const answerBox = document.getElementById("answerBox");

    if (!query) {
        alert("Enter a question");
        return;
    }

    const formData = new URLSearchParams();
    formData.append("query", query);

    try {
        const res = await fetch("http://127.0.0.1:8000/ask", {
            method: "POST",
            body: formData,
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            }
        });

        const data = await res.json();
        answerBox.innerText = data.answer;

    } catch (err) {
        console.error(err);
        alert("Ask failed");
    }
}