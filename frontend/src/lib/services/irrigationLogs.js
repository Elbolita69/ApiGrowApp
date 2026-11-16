// Servicios del historial de riego (API principal, FastAPI).
import { request } from './api.js';

const BASE = '/irrigation-logs';

/** Lista de registros de riego. */
export async function listar() {
	return request(`${BASE}/`);
}

/** Un registro por identificador (el id solo se usa internamente). @param {number|string} id */
export async function obtener(id) {
	return request(`${BASE}/${id}`);
}

/** Registra una operacion de riego. @param {Record<string, any>} datos */
export async function crear(datos) {
	return request(`${BASE}/`, { method: 'POST', body: datos });
}

/** Actualiza un registro de riego. @param {number|string} id @param {Record<string, any>} datos */
export async function actualizar(id, datos) {
	return request(`${BASE}/${id}`, { method: 'PUT', body: datos });
}

/** Elimina (borrado logico en la API) un registro de riego. @param {number|string} id */
export async function eliminar(id) {
	return request(`${BASE}/${id}`, { method: 'DELETE' });
}
