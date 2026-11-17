import { request } from './api.js';

export async function login(username, password) {
	return request('/auth/login', { method: 'POST', form: { username, password } });
}

export async function me() {
	return request('/auth/me');
}

export async function modulos() {
	return request('/auth/modulos');
}
