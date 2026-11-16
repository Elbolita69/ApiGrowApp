// Servicios de alertas (API principal, FastAPI).
import { request } from './api.js';

const BASE = '/alerts';

/** Lista de alertas. */
export async function listar() {
	return request(`${BASE}/`);
}

/** Una alerta por identificador (el id solo se usa internamente). @param {number|string} id */
export async function obtener(id) {
	return request(`${BASE}/${id}`);
}

/** Registra una alerta. @param {Record<string, any>} datos */
export async function crear(datos) {
	return request(`${BASE}/`, { method: 'POST', body: datos });
}

/** Actualiza una alerta. @param {number|string} id @param {Record<string, any>} datos */
export async function actualizar(id, datos) {
	return request(`${BASE}/${id}`, { method: 'PUT', body: datos });
}

/** Elimina (borrado logico en la API) una alerta. @param {number|string} id */
export async function eliminar(id) {
	return request(`${BASE}/${id}`, { method: 'DELETE' });
}
