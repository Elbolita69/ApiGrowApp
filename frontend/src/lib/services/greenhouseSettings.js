// Servicios de parametros por invernadero (API principal, FastAPI).
// En esta API los parametros se editan y eliminan por invernadero, no por id de parametro.
import { request } from './api.js';

const BASE = '/greenhouse-settings';

/** Lista de parametros. */
export async function listar() {
	return request(`${BASE}/`);
}

/** Parametros de un invernadero (el id solo se usa internamente). @param {number|string} greenhouseId */
export async function obtener(greenhouseId) {
	return request(`${BASE}/greenhouse/${greenhouseId}`);
}

/** Crea los parametros de un invernadero. @param {Record<string, any>} datos */
export async function crear(datos) {
	return request(`${BASE}/`, { method: 'POST', body: datos });
}

/** Actualiza los parametros de un invernadero. @param {number|string} greenhouseId @param {Record<string, any>} datos */
export async function actualizar(greenhouseId, datos) {
	return request(`${BASE}/greenhouse/${greenhouseId}`, { method: 'PUT', body: datos });
}

/** Elimina (borrado logico en la API) los parametros de un invernadero. @param {number|string} greenhouseId */
export async function eliminar(greenhouseId) {
	return request(`${BASE}/greenhouse/${greenhouseId}`, { method: 'DELETE' });
}
