import { goto } from '$app/navigation';
import { API_URL, EXPRESS_URL } from './config.js';
import { session, cerrarSesion } from './stores/session.svelte.js';

/**
 * Peticion generica a una de las dos APIs.
 * base: 'fastapi' (con token JWT) | 'express' (API auxiliar, sin autenticacion)
 */
export async function request(base, path, { method = 'GET', body, form } = {}) {
	const headers = {};
	let payload;
	if (form) {
		headers['Content-Type'] = 'application/x-www-form-urlencoded';
		payload = new URLSearchParams(form).toString();
	} else if (body !== undefined) {
		headers['Content-Type'] = 'application/json';
		payload = JSON.stringify(body);
	}
	if (base === 'fastapi' && session.token) headers.Authorization = `Bearer ${session.token}`;

	let res;
	try {
		res = await fetch((base === 'express' ? EXPRESS_URL : API_URL) + path, {
			method,
			headers,
			body: payload
		});
	} catch {
		throw new Error('No se pudo conectar con el servidor. Verifica que la API este encendida.');
	}

	if (res.status === 401 && base === 'fastapi' && session.token) {
		cerrarSesion();
		goto('/login');
		throw new Error('Tu sesion expiro. Inicia sesion de nuevo.');
	}
	if (!res.ok) {
		let mensaje = `Error ${res.status}`;
		try {
			const j = await res.json();
			if (typeof j.detail === 'string') mensaje = j.detail;
			else if (Array.isArray(j.detail)) mensaje = j.detail.map((d) => d.msg).join(', ');
			else if (j.error) mensaje = j.error;
		} catch {
			/* sin cuerpo JSON */
		}
		throw new Error(mensaje);
	}
	return res.status === 204 ? null : res.json();
}

export const api = {
	get: (path, base = 'fastapi') => request(base, path),
	post: (path, body, base = 'fastapi') => request(base, path, { method: 'POST', body }),
	put: (path, body, base = 'fastapi') => request(base, path, { method: 'PUT', body }),
	delete: (path, base = 'fastapi') => request(base, path, { method: 'DELETE' })
};
