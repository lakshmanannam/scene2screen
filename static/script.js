async function startGeneration() {
    const prompt = document.getElementById('userPrompt').value;
    const response = await fetch('/generate_content', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ prompt: prompt })
    });
    
    const result = await response.json();
    if (result.status === "success") {
        document.getElementById('storyDisplay').innerText = result.story;
    } else {
        alert("Error: " + result.message);
    }
}
