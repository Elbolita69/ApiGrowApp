// Servicios de ordenes de control de actuadores (API principal, FastAPI).
import { request } from './api.js';

const BASE = '/actuator-controls';

/** Lista de ordenes de control. */
export async function listar() {
	return request(`${BASE}/`);
}

/** Una orden por identificador (el id solo se usa internamente). @param {number|string} id */
export async function obtener(id) {
	return request(`${BASE}/${id}`);
}

/** Crea una orden de control. @param {Record<string, any>} datos */
export async function crear(datos) {
	return request(`${BASE}/`, { method: 'POST', body: datos });
}

/** Actualiza una orden de control. @param {number|string} id @param {Record<string, any>} datos */
export async function actualizar(id, datos) {
	return request(`${BASE}/${id}`, { method: 'PUT', body: datos });
}

/** Elimina (borrado logico en la API) una orden de control. @param {number|string} id */
export async function eliminar(id) {
	return request(`${BASE}/${id}`, { method: 'DELETE' });
}
