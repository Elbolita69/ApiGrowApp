const API_BASE = 'https://apigrowapp.onrender.com';

document.querySelectorAll('nav button').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('nav button').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById(btn.dataset.section).classList.add('active');
        loadSection(btn.dataset.section);
    });
});

function openModal(id) {
    document.getElementById(id).classList.add('active');
}

function closeModal(id) {
    document.getElementById(id).classList.remove('active');
}

document.querySelectorAll('.modal').forEach(modal => {
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('active');
        }
    });
});

async function apiGet(endpoint) {
    const res = await fetch(`${API_BASE}${endpoint}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
}

async function apiPost(endpoint, data) {
    const res = await fetch(`${API_BASE}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
}

async function apiDelete(endpoint) {
    const res = await fetch(`${API_BASE}${endpoint}`, { method: 'DELETE' });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
}

async function loadSection(section) {
    switch(section) {
        case 'dashboard': loadDashboard(); break;
        case 'greenhouses': loadGreenhouses(); break;
        case 'sensors': loadSensors(); break;
        case 'readings': loadReadings(); break;
        case 'crops': loadCrops(); break;
        case 'batches': loadBatches(); break;
        case 'alerts': loadAlerts(); break;
        case 'irrigation': loadIrrigation(); break;
        case 'actuators': loadActuators(); break;
        case 'settings': loadSettings(); break;
        case 'users': loadUsers(); break;
    }
}

async function loadDashboard() {
    try {
        const [ghouses, alerts, readings] = await Promise.all([
            apiGet('/greenhouses/'),
            apiGet('/alerts/activas'),
            apiGet('/sensor-readings/')
        ]);

        document.getElementById('stat-greenhouses').textContent = ghouses.length || 0;
        document.getElementById('stat-alerts').textContent = alerts.length || 0;

        const temps = readings.filter(r => r.tipo === 'temperatura').slice(0, 10);
        const humids = readings.filter(r => r.tipo === 'humedad').slice(0, 10);

        if (temps.length) {
            const avg = (temps.reduce((s, r) => s + parseFloat(r.valor), 0) / temps.length).toFixed(1);
            document.getElementById('stat-temp').textContent = avg + '°C';
        }
        if (humids.length) {
            const avg = (humids.reduce((s, r) => s + parseFloat(r.valor), 0) / humids.length).toFixed(1);
            document.getElementById('stat-humidity').textContent = avg + '%';
        }

        const readingsHtml = readings.slice(0, 10).length ? `
            <table>
                <thead><tr><th>Sensor</th><th>Tipo</th><th>Valor</th><th>Timestamp</th></tr></thead>
                <tbody>
                    ${readings.slice(0, 10).map(r => `
                        <tr>
                            <td>${r.sensor_nombre || r.sensor_id}</td>
                            <td><span class="badge badge-info">${r.tipo}</span></td>
                            <td><strong>${r.valor} ${r.unidad || ''}</strong></td>
                            <td>${new Date(r.timestamp).toLocaleString()}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        ` : '<div class="empty-state">No hay lecturas registradas</div>';
        document.getElementById('latest-readings').innerHTML = readingsHtml;

        const alertsHtml = alerts.length ? `
            <table>
                <thead><tr><th>Tipo</th><th>Mensaje</th><th>Prioridad</th><th>Timestamp</th><th>Acción</th></tr></thead>
                <tbody>
                    ${alerts.map(a => `
                        <tr>
                            <td>${a.tipo}</td>
                            <td>${a.mensaje}</td>
                            <td><span class="badge ${a.prioridad === 'critica' ? 'badge-danger' : a.prioridad === 'alta' ? 'badge-warning' : 'badge-info'}">${a.prioridad}</span></td>
                            <td>${new Date(a.timestamp).toLocaleString()}</td>
                            <td><button class="btn btn-sm btn-primary" onclick="resolveAlert(${a.id})">Resolver</button></td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        ` : '<div class="empty-state">No hay alertas activas</div>';
        document.getElementById('active-alerts').innerHTML = alertsHtml;

    } catch (e) {
        console.error('Dashboard error:', e);
    }
}

async function loadGreenhouses() {
    try {
        const data = await apiGet('/greenhouses/');
        const html = data.length ? `
            <table>
                <thead><tr><th>ID</th><th>Nombre</th><th>Ubicación</th><th>Área (m²)</th><th>Capacidad</th><th>Estado</th></tr></thead>
                <tbody>
                    ${data.map(g => `
                        <tr>
                            <td>${g.id}</td>
                            <td><strong>${g.nombre}</strong></td>
                            <td>${g.ubicacion || '-'}</td>
                            <td>${g.area_metros_cuadrados || '-'}</td>
                            <td>${g.capacidad_maxima || '-'}</td>
                            <td><span class="badge badge-success">${g.estado}</span></td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        ` : '<div class="empty-state">No hay invernaderos registrados</div>';
        document.getElementById('greenhouses-list').innerHTML = html;
    } catch (e) {
        document.getElementById('greenhouses-list').innerHTML = '<div class="empty-state">Error al cargar datos</div>';
    }
}

async function loadSensors() {
    try {
        const data = await apiGet('/sensors/');
        const html = data.length ? `
            <table>
                <thead><tr><th>ID</th><th>Nombre</th><th>Tipo</th><th>Unidad</th><th>Ubicación</th><th>Estado</th></tr></thead>
                <tbody>
                    ${data.map(s => `
                        <tr>
                            <td>${s.id}</td>
                            <td><strong>${s.nombre}</strong></td>
                            <td><span class="badge badge-info">${s.tipo}</span></td>
                            <td>${s.unidad}</td>
                            <td>${s.ubicacion || '-'}</td>
                            <td><span class="badge badge-success">${s.estado}</span></td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        ` : '<div class="empty-state">No hay sensores registrados</div>';
        document.getElementById('sensors-list').innerHTML = html;
    } catch (e) {
        document.getElementById('sensors-list').innerHTML = '<div class="empty-state">Error al cargar datos</div>';
    }
}

async function loadReadings() {
    try {
        const data = await apiGet('/sensor-readings/');
        const html = data.length ? `
            <table>
                <thead><tr><th>ID</th><th>Sensor</th><th>Tipo</th><th>Valor</th><th>Timestamp</th></tr></thead>
                <tbody>
                    ${data.map(r => `
                        <tr>
                            <td>${r.id}</td>
                            <td>${r.sensor_nombre || r.sensor_id}</td>
                            <td><span class="badge badge-info">${r.tipo}</span></td>
                            <td><strong>${r.valor} ${r.unidad || ''}</strong></td>
                            <td>${new Date(r.timestamp).toLocaleString()}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        ` : '<div class="empty-state">No hay lecturas registradas</div>';
        document.getElementById('readings-list').innerHTML = html;
    } catch (e) {
        document.getElementById('readings-list').innerHTML = '<div class="empty-state">Error al cargar datos</div>';
    }
}

async function loadCrops() {
    try {
        const data = await apiGet('/crops/');
        const html = data.length ? `
            <table>
                <thead><tr><th>ID</th><th>Nombre</th><th>Nombre Científico</th><th>Temp.</th><th>Humedad</th><th>Ciclo</th></tr></thead>
                <tbody>
                    ${data.map(c => `
                        <tr>
                            <td>${c.id}</td>
                            <td><strong>${c.nombre}</strong></td>
                            <td><em>${c.nombre_cientifico || '-'}</em></td>
                            <td>${c.temperatura_min || '-'} - ${c.temperatura_max || '-'} °C</td>
                            <td>${c.humedad_min || '-'} - ${c.humedad_max || '-'} %</td>
                            <td>${c.ciclo_dias || '-'} días</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        ` : '<div class="empty-state">No hay cultivos registrados</div>';
        document.getElementById('crops-list').innerHTML = html;
    } catch (e) {
        document.getElementById('crops-list').innerHTML = '<div class="empty-state">Error al cargar datos</div>';
    }
}

async function loadBatches() {
    try {
        const data = await apiGet('/crop-batches/');
        const html = data.length ? `
            <table>
                <thead><tr><th>ID</th><th>Cultivo</th><th>Fecha Siembra</th><th>Cosecha Est.</th><th>Plantas</th><th>Estado</th></tr></thead>
                <tbody>
                    ${data.map(b => `
                        <tr>
                            <td>${b.id}</td>
                            <td>${b.cultivo_nombre || b.crop_id}</td>
                            <td>${b.fecha_siembra}</td>
                            <td>${b.fecha_cosecha_estimada || '-'}</td>
                            <td>${b.cantidad_plantas || '-'}</td>
                            <td><span class="badge badge-success">${b.estado}</span></td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        ` : '<div class="empty-state">No hay lotes registrados</div>';
        document.getElementById('batches-list').innerHTML = html;
    } catch (e) {
        document.getElementById('batches-list').innerHTML = '<div class="empty-state">Error al cargar datos</div>';
    }
}

async function loadAlerts() {
    try {
        const data = await apiGet('/alerts/');
        const html = data.length ? `
            <table>
                <thead><tr><th>ID</th><th>Tipo</th><th>Mensaje</th><th>Prioridad</th><th>Estado</th><th>Timestamp</th></tr></thead>
                <tbody>
                    ${data.map(a => `
                        <tr>
                            <td>${a.id}</td>
                            <td>${a.tipo}</td>
                            <td>${a.mensaje}</td>
                            <td><span class="badge ${a.prioridad === 'critica' ? 'badge-danger' : a.prioridad === 'alta' ? 'badge-warning' : 'badge-info'}">${a.prioridad}</span></td>
                            <td><span class="badge ${a.estado === 'activa' ? 'badge-danger' : 'badge-success'}">${a.estado}</span></td>
                            <td>${new Date(a.timestamp).toLocaleString()}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        ` : '<div class="empty-state">No hay alertas registradas</div>';
        document.getElementById('alerts-list').innerHTML = html;
    } catch (e) {
        document.getElementById('alerts-list').innerHTML = '<div class="empty-state">Error al cargar datos</div>';
    }
}

async function loadIrrigation() {
    try {
        const [zones, logs] = await Promise.all([
            apiGet('/irrigation-zones/'),
            apiGet('/irrigation-logs/')
        ]);

        const zonesHtml = zones.length ? `
            <table>
                <thead><tr><th>ID</th><th>Nombre</th><th>Invernadero</th><th>Tipo</th><th>Estado</th></tr></thead>
                <tbody>
                    ${zones.map(z => `
                        <tr>
                            <td>${z.id}</td>
                            <td><strong>${z.nombre}</strong></td>
                            <td>${z.greenhouse_nombre || z.greenhouse_id}</td>
                            <td>${z.tipo}</td>
                            <td><span class="badge badge-success">${z.estado}</span></td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        ` : '<div class="empty-state">No hay zonas de riego</div>';
        document.getElementById('zones-list').innerHTML = zonesHtml;

        const logsHtml = logs.length ? `
            <table>
                <thead><tr><th>ID</th><th>Zona</th><th>Duración</th><th>Agua (L)</th><th>Modo</th><th>Resultado</th><th>Timestamp</th></tr></thead>
                <tbody>
                    ${logs.map(l => `
                        <tr>
                            <td>${l.id}</td>
                            <td>${l.zone_nombre || l.zone_id}</td>
                            <td>${l.duracion_minutos} min</td>
                            <td>${l.cantidad_agua_litros || '-'}</td>
                            <td>${l.modo}</td>
                            <td><span class="badge ${l.resultado === 'exitoso' ? 'badge-success' : 'badge-danger'}">${l.resultado}</span></td>
                            <td>${new Date(l.creado).toLocaleString()}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        ` : '<div class="empty-state">No hay historial de riego</div>';
        document.getElementById('irrigation-logs').innerHTML = logsHtml;
    } catch (e) {
        document.getElementById('zones-list').innerHTML = '<div class="empty-state">Error al cargar zonas: ' + e.message + '</div>';
        document.getElementById('irrigation-logs').innerHTML = '<div class="empty-state">Error al cargar historial</div>';
    }
}

async function loadActuators() {
    try {
        const [actuators, controls] = await Promise.all([
            apiGet('/actuators/'),
            apiGet('/actuator-controls/')
        ]);

        const actuatorsHtml = actuators.length ? `
            <table>
                <thead><tr><th>ID</th><th>Nombre</th><th>Tipo</th><th>Ubicación</th><th>Estado</th></tr></thead>
                <tbody>
                    ${actuators.map(a => `
                        <tr>
                            <td>${a.id}</td>
                            <td><strong>${a.nombre}</strong></td>
                            <td><span class="badge badge-info">${a.tipo}</span></td>
                            <td>${a.ubicacion || '-'}</td>
                            <td><span class="badge ${a.estado === 'activo' ? 'badge-success' : 'badge-warning'}">${a.estado}</span></td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        ` : '<div class="empty-state">No hay actuadores registrados</div>';
        document.getElementById('actuators-list').innerHTML = actuatorsHtml;

        const controlsHtml = controls.length ? `
            <table>
                <thead><tr><th>ID</th><th>Actuador</th><th>Acción</th><th>Valor</th><th>Resultado</th><th>Timestamp</th></tr></thead>
                <tbody>
                    ${controls.map(c => `
                        <tr>
                            <td>${c.id}</td>
                            <td>${c.actuator_nombre || c.actuator_id}</td>
                            <td>${c.accion}</td>
                            <td>${c.valor_ajuste || '-'}</td>
                            <td><span class="badge ${c.resultado === 'exitoso' ? 'badge-success' : 'badge-danger'}">${c.resultado}</span></td>
                            <td>${new Date(c.timestamp).toLocaleString()}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        ` : '<div class="empty-state">No hay controles registrados</div>';
        document.getElementById('actuator-controls').innerHTML = controlsHtml;
    } catch (e) {
        console.error('Actuators error:', e);
    }
}

async function loadSettings() {
    try {
        const data = await apiGet('/greenhouse-settings/');
        const html = data.length ? `
            <table>
                <thead><tr><th>ID</th><th>Invernadero</th><th>Temp.</th><th>Humedad</th><th>pH</th><th>Intervalo</th></tr></thead>
                <tbody>
                    ${data.map(s => `
                        <tr>
                            <td>${s.id}</td>
                            <td><strong>${s.greenhouse_nombre || s.greenhouse_id}</strong></td>
                            <td>${s.temp_min} - ${s.temp_max} °C</td>
                            <td>${s.humedad_min} - ${s.humedad_max} %</td>
                            <td>${s.ph_min} - ${s.ph_max}</td>
                            <td>${s.intervalo_lectura_minutos} min</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        ` : '<div class="empty-state">No hay configuraciones</div>';
        document.getElementById('settings-list').innerHTML = html;
    } catch (e) {
        document.getElementById('settings-list').innerHTML = '<div class="empty-state">Error al cargar datos</div>';
    }
}

async function loadUsers() {
    try {
        const data = await apiGet('/users/');
        const html = data.length ? `
            <table>
                <thead><tr><th>ID</th><th>Username</th><th>Email</th><th>Nombre</th><th>Rol</th><th>Estado</th></tr></thead>
                <tbody>
                    ${data.map(u => `
                        <tr>
                            <td>${u.id}</td>
                            <td><strong>${u.username}</strong></td>
                            <td>${u.email}</td>
                            <td>${u.nombre || '-'}</td>
                            <td><span class="badge badge-info">${u.rol}</span></td>
                            <td><span class="badge badge-success">${u.estado}</span></td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        ` : '<div class="empty-state">No hay usuarios registrados</div>';
        document.getElementById('users-list').innerHTML = html;
    } catch (e) {
        document.getElementById('users-list').innerHTML = '<div class="empty-state">Error al cargar datos</div>';
    }
}

async function resolveAlert(id) {
    try {
        await fetch(`${API_BASE}/alerts/${id}/resolver`, { method: 'PATCH' });
        loadDashboard();
    } catch (e) {
        alert('Error al resolver alerta');
    }
}

function cleanFormData(formData) {
    const obj = {};
    for (const [key, value] of formData.entries()) {
        if (value === '' || value === null) {
            obj[key] = null;
        } else if (!isNaN(value) && value !== '' && !value.match(/^\d{4}-\d{2}-\d{2}/)) {
            const num = parseFloat(value);
            // Treat 0 as null for _id fields (foreign keys can't be 0)
            obj[key] = (num === 0 && key.endsWith('_id')) ? null : num;
        } else {
            obj[key] = value;
        }
    }
    return obj;
}

document.getElementById('greenhouse-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = cleanFormData(new FormData(e.target));
    try {
        await apiPost('/greenhouses/', data);
        closeModal('greenhouse-modal');
        loadGreenhouses();
        e.target.reset();
    } catch (err) {
        alert('Error al crear invernadero: ' + err.message);
    }
});

document.getElementById('sensor-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = cleanFormData(new FormData(e.target));
    try {
        await apiPost('/sensors/', data);
        closeModal('sensor-modal');
        loadSensors();
        e.target.reset();
    } catch (err) {
        alert('Error al crear sensor: ' + err.message);
    }
});

document.getElementById('crop-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = cleanFormData(new FormData(e.target));
    try {
        await apiPost('/crops/', data);
        closeModal('crop-modal');
        loadCrops();
        e.target.reset();
    } catch (err) {
        alert('Error al crear cultivo: ' + err.message);
    }
});

document.getElementById('zone-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = cleanFormData(new FormData(e.target));
    try {
        await apiPost('/irrigation-zones/', data);
        closeModal('zone-modal');
        loadIrrigation();
        e.target.reset();
    } catch (err) {
        alert('Error al crear zona: ' + err.message);
    }
});

document.getElementById('batch-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = cleanFormData(new FormData(e.target));
    try {
        await apiPost('/crop-batches/', data);
        closeModal('batch-modal');
        loadBatches();
        e.target.reset();
    } catch (err) {
        alert('Error al crear lote: ' + err.message);
    }
});

document.getElementById('actuator-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = cleanFormData(new FormData(e.target));
    try {
        await apiPost('/actuators/', data);
        closeModal('actuator-modal');
        loadActuators();
        e.target.reset();
    } catch (err) {
        alert('Error al crear actuador: ' + err.message);
    }
});

document.getElementById('user-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = cleanFormData(new FormData(e.target));
    try {
        await apiPost('/users/', data);
        closeModal('user-modal');
        loadUsers();
        e.target.reset();
    } catch (err) {
        alert('Error al crear usuario: ' + err.message);
    }
});

loadDashboard();
