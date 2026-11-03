function handleLogin() {
    const user = document.getElementById('username').value;
    const pass = document.getElementById('password').value;
    const errorMsg = document.getElementById('login-error');

    if (user === "admin" && pass === "admin") {
        document.getElementById('login-screen').style.display = 'none';
        document.getElementById('dashboard-screen').style.display = 'grid';
    } else {
        errorMsg.style.display = 'block';
    }
}

async function sendCmd(command) {
    const response = await fetch('/cmd/' + command, { method: 'POST' });
    const data = await response.json();
    document.getElementById('status-display').innerText = "Status: " + data.status;
}
