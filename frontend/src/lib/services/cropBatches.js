import { request } from './api.js';

const BASE = '/crop-batches';

export async function listar() {
	return request(`${BASE}/`);
}

export async function obtener(id) {
	return request(`${BASE}/${id}`);
}

export async function crear(datos) {
	return request(`${BASE}/`, { method: 'POST', body: datos });
}

export async function actualizar(id, datos) {
	return request(`${BASE}/${id}`, { method: 'PUT', body: datos });
}

export async function eliminar(id) {
	return request(`${BASE}/${id}`, { method: 'DELETE' });
}
