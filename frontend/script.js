async function getRecommendations() {

    const query = document.getElementById("query").value;

    const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            messages: [
                {
                    role: "user",
                    content: query
                }
            ]
        })
    });

    const data = await response.json();

    const resultsDiv = document.getElementById("results");

    resultsDiv.innerHTML = "";

    data.recommendations.forEach(rec => {

        resultsDiv.innerHTML += `
            <div class="card">
                <h3>${rec.name}</h3>
                <p>${rec.description}</p>
                <a href="${rec.url}" target="_blank">
                    View Assessment
                </a>
            </div>
        `;
    });
}