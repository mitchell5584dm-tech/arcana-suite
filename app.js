async function sendCommand() {
    const cmd = document.getElementById("cmdInput").value;

    const res = await fetch("/command", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({cmd})
    });

    document.getElementById("cmdOutput").innerText = JSON.stringify(await res.json(), null, 2);
}

async function runInstall() {
    const config = {
        path: "/usr/local/arcana",
        permissions: "user",
        network_mode: "offline"
    };

    const res = await fetch("/install", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(config)
    });

    document.getElementById("installOutput").innerText = JSON.stringify(await res.json(), null, 2);
}

async function getPlan(plan) {
    const res = await fetch(`/subscription/${plan}`);
    document.getElementById("subOutput").innerText = JSON.stringify(await res.json(), null, 2);
}

