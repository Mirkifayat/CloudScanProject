async function startScan() {
    const target = document.getElementById('target').value;
    const btn = document.getElementById('scan-btn');
    const loader = document.getElementById('loader');
    const resultContainer = document.getElementById('result-container');
    const output = document.getElementById('output');

    if (!target) {
        alert("Please enter a target!");
        return;
    }

    btn.disabled = true;
    loader.classList.remove('hidden');
    resultContainer.classList.add('hidden');

    try {
        // This sends the data to your app.py
        const response = await fetch('/scan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ target: target })
        });

        const data = await response.json();

        loader.classList.add('hidden');
        resultContainer.classList.remove('hidden');

        if (response.ok) {
            output.textContent = data.results;
        } else {
            output.textContent = `Error: ${data.error}\n${data.details || ''}`;
        }
    } catch (error) {
        alert("Could not connect to the backend server.");
    } finally {
        btn.disabled = false;
    }
}