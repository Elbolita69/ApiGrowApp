// Servicios del asistente de consultas a la base de datos (API principal, FastAPI).
// Regla del taller: el asistente responde SIEMPRE en lenguaje natural, nunca muestra SQL.
import { request } from './api.js';

/**
 * Envia una pregunta al asistente.
 * @param {string} pregunta pregunta en lenguaje natural
 * @returns {Promise<{respuesta: string}>}
 */
export async function preguntar(pregunta) {
	return request('/asistente/preguntar', { method: 'POST', body: { pregunta } });
}
