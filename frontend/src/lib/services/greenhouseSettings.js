import { request } from './api.js';

const BASE = '/greenhouse-settings';

export async function listar() {
	return request(`${BASE}/`);
}

export async function obtener(greenhouseId) {
	return request(`${BASE}/greenhouse/${greenhouseId}`);
}

export async function crear(datos) {
	return request(`${BASE}/`, { method: 'POST', body: datos });
}

export async function actualizar(greenhouseId, datos) {
	return request(`${BASE}/greenhouse/${greenhouseId}`, { method: 'PUT', body: datos });
}

export async function eliminar(greenhouseId) {
	return request(`${BASE}/greenhouse/${greenhouseId}`, { method: 'DELETE' });
}
