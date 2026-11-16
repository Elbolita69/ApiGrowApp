// Servicios de autenticacion y permisos (API principal, FastAPI).
import { request } from './api.js';

/**
 * Inicia sesion. El backend espera form-urlencoded (OAuth2PasswordRequestForm).
 * @param {string} username
 * @param {string} password
 * @returns {Promise<{access_token: string, token_type: string}>}
 */
export async function login(username, password) {
	return request('/auth/login', { method: 'POST', form: { username, password } });
}

/** Datos del usuario con la sesion actual. */
export async function me() {
	return request('/auth/me');
}

/** Modulos y permisos del rol (tabla moduloxrol). */
export async function modulos() {
	return request('/auth/modulos');
}
