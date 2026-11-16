// Servicios de lotes de cultivo (API principal, FastAPI).
import { request } from './api.js';

const BASE = '/crop-batches';

/** Lista de lotes. */
export async function listar() {
	return request(`${BASE}/`);
}

/** Un lote por identificador (el id solo se usa internamente). @param {number|string} id */
export async function obtener(id) {
	return request(`${BASE}/${id}`);
}

/** Crea un lote de cultivo. @param {Record<string, any>} datos */
export async function crear(datos) {
	return request(`${BASE}/`, { method: 'POST', body: datos });
}

/** Actualiza un lote de cultivo. @param {number|string} id @param {Record<string, any>} datos */
export async function actualizar(id, datos) {
	return request(`${BASE}/${id}`, { method: 'PUT', body: datos });
}

/** Elimina (borrado logico en la API) un lote de cultivo. @param {number|string} id */
export async function eliminar(id) {
	return request(`${BASE}/${id}`, { method: 'DELETE' });
}
