// Servicios de invernaderos (API principal, FastAPI).
import { request } from './api.js';

const BASE = '/greenhouses';

/** Lista de invernaderos. */
export async function listar() {
	return request(`${BASE}/`);
}

/** Un invernadero por identificador (el id solo se usa internamente). @param {number|string} id */
export async function obtener(id) {
	return request(`${BASE}/${id}`);
}

/** Crea un invernadero. @param {Record<string, any>} datos */
export async function crear(datos) {
	return request(`${BASE}/`, { method: 'POST', body: datos });
}

/** Actualiza un invernadero. @param {number|string} id @param {Record<string, any>} datos */
export async function actualizar(id, datos) {
	return request(`${BASE}/${id}`, { method: 'PUT', body: datos });
}

/** Elimina (borrado logico en la API) un invernadero. @param {number|string} id */
export async function eliminar(id) {
	return request(`${BASE}/${id}`, { method: 'DELETE' });
}
