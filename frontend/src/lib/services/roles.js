// Servicios de roles (API principal, FastAPI).
import { request } from './api.js';

const BASE = '/roles';

/** Lista de roles. */
export async function listar() {
	return request(`${BASE}/`);
}

/** Un rol por identificador (el id solo se usa internamente). @param {number|string} id */
export async function obtener(id) {
	return request(`${BASE}/${id}`);
}

/** Crea un rol. @param {Record<string, any>} datos */
export async function crear(datos) {
	return request(`${BASE}/`, { method: 'POST', body: datos });
}

/** Actualiza un rol. @param {number|string} id @param {Record<string, any>} datos */
export async function actualizar(id, datos) {
	return request(`${BASE}/${id}`, { method: 'PUT', body: datos });
}

/** Elimina (borrado logico en la API) un rol. @param {number|string} id */
export async function eliminar(id) {
	return request(`${BASE}/${id}`, { method: 'DELETE' });
}
