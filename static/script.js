// Local store for login credentials
const users = {
    "admin": "admin"
};

// Handle login validation
function handleLogin() {
    const user = document.getElementById('username').value.trim();
    const pass = document.getElementById('password').value.trim();
    const errorMsg = document.getElementById('login-error');

    if (users[user] && users[user] === pass) {
        document.getElementById('login-screen').style.display = 'none';
        document.getElementById('dashboard-screen').style.display = 'grid';
        errorMsg.style.display = 'none';
    } else {
        errorMsg.innerText = "Invalid username or password";
        errorMsg.style.display = 'block';
    }
}

// Handle new account registration
function handleRegister() {
    const user = document.getElementById('username').value.trim();
    const pass = document.getElementById('password').value.trim();
    const errorMsg = document.getElementById('login-error');

    if (!user || !pass) {
        errorMsg.innerText = "Please enter both username & password";
        errorMsg.style.display = 'block';
        return;
    }

    if (users[user]) {
        errorMsg.innerText = "Account already exists!";
        errorMsg.style.display = 'block';
        return;
    }

    users[user] = pass;
    alert("Account created successfully! You can now log in.");
    errorMsg.style.display = 'none';
}

// Send command POST request to Python backend
async function sendCmd(command) {
    const response = await fetch('/cmd/' + command, { method: 'POST' });
    const data = await response.json();
    document.getElementById('status-display').innerText = "Status: " + data.status;
}
