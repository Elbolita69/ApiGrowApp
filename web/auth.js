const API_BASE = 'https://apigrowapp.onrender.com';
const TOKEN_KEY = 'access_token';

function getToken() { return localStorage.getItem(TOKEN_KEY); }
function setToken(token) { localStorage.setItem(TOKEN_KEY, token); }
function clearToken() { localStorage.removeItem(TOKEN_KEY); }

function getHeaders() {
    const token = getToken();
    return token ? { 'Authorization': `Bearer ${token}` } : {};
}

function showApp() {
    document.getElementById('login-section').classList.remove('active');
    document.getElementById('login-section').style.display = 'none';
    document.getElementById('register-section').style.display = 'none';
    document.querySelector('nav').style.display = 'flex';
    document.querySelector('main').style.display = 'block';
}

function showLogin() {
    document.getElementById('login-section').style.display = 'block';
    document.getElementById('login-section').classList.add('active');
    document.getElementById('register-section').style.display = 'none';
    document.querySelector('nav').style.display = 'none';
    document.querySelector('main').style.display = 'none';
}

function showRegister() {
    document.getElementById('login-section').style.display = 'none';
    document.getElementById('register-section').style.display = 'block';
    document.getElementById('register-section').classList.add('active');
    document.querySelector('nav').style.display = 'none';
    document.querySelector('main').style.display = 'none';
}

function checkAuth() {
    const token = getToken();
    if (!token) {
        showLogin();
        return;
    }
    showApp();
    loadDashboard();
}

async function login(username, password) {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    const res = await fetch(`${API_BASE}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formData
    });
    if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Login fallido');
    }
    const data = await res.json();
    setToken(data.access_token);
    showApp();
    loadDashboard();
}

async function registerUser(username, email, nombre, password) {
    const res = await fetch(`${API_BASE}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, nombre, password, rol_id: 2 })
    });
    if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Registro fallido');
    }
    showLogin();
    alert('Cuenta creada. Puedes iniciar sesión.');
}

function logout() {
    clearToken();
    showLogin();
}

// Login form
document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    try {
        await login(fd.get('username'), fd.get('password'));
        e.target.reset();
    } catch (err) {
        alert('Error: ' + err.message);
    }
});

// Register form
document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    try {
        await registerUser(fd.get('username'), fd.get('email'), fd.get('nombre'), fd.get('password'));
        e.target.reset();
    } catch (err) {
        alert('Error: ' + err.message);
    }
});
