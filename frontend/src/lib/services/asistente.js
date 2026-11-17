import { request } from './api.js';

export async function preguntar(pregunta) {
	return request('/asistente/preguntar', { method: 'POST', body: { pregunta } });
}
