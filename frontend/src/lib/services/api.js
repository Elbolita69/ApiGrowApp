import { goto } from '$app/navigation';
import { session, cerrarSesion } from '#lib/stores/session.svelte.js';
import { BASE_FASTAPI, BASE_EXPRESS } from '#lib/config.js';

export { BASE_FASTAPI, BASE_EXPRESS };

const PREFIJOS = {
	fastapi: BASE_FASTAPI,
	express: BASE_EXPRESS
};

const TRADUCCIONES = {
	'field required': 'campo obligatorio',
	'Input should be a valid integer': 'debe ser un numero entero',
	'Input should be a valid number': 'debe ser un numero',
	'Input should be a valid string': 'debe ser texto',
	'Input should be a valid boolean': 'debe ser verdadero o falso',
	'Input should be a valid list': 'debe ser una lista',
	'Input should be a valid dictionary or object to extract fields from': 'el formato del objeto no es valido',
	'Input should be a valid date or datetime': 'debe ser una fecha valida',
	'value is not a valid email address': 'no es un correo electronico valido',
	'value is not a valid decimal number': 'no es un numero valido',
	'string should match pattern': 'el formato no es valido',
	'ensure this value is less than or equal to': 'debe ser menor o igual a',
	'ensure this value is greater than or equal to': 'debe ser mayor o igual a',
	'ensure this value is less than': 'debe ser menor que',
	'ensure this value is greater than': 'debe ser mayor que'
};

function traducir(mensaje) {
	const texto = String(mensaje ?? '').trim();
	if (!texto) return '';
	const exacto = TRADUCCIONES[texto.toLowerCase()];
	if (exacto) return exacto;
	for (const [clave, valor] of Object.entries(TRADUCCIONES)) {
		if (texto.toLowerCase().startsWith(clave)) {
			return valor + texto.slice(clave.length);
		}
	}
	return texto;
}

function mensajeDeDetalle(detalle) {
	if (detalle === null || detalle === undefined) return '';
	if (typeof detalle === 'string') return traducir(detalle);
	if (Array.isArray(detalle)) {
		const partes = detalle
			.map((item) => {
				if (typeof item === 'string') return traducir(item);
				const mensaje = item?.msg ?? item?.message ?? '';
				const ubicacion = Array.isArray(item?.loc) ? item.loc[item.loc.length - 1] : item?.loc;
				const texto = traducir(mensaje);
				if (!texto) return '';
				return ubicacion && ubicacion !== 'body' ? `${ubicacion}: ${texto}` : texto;
			})
			.filter(Boolean);
		return partes.join('. ');
	}
	if (typeof detalle === 'object') {
		const campos = (detalle);
		const mensaje = campos.msg ?? campos.message ?? campos.error;
		return mensaje ? traducir(mensaje) : '';
	}
	return '';
}

async function mensajeDeError(res) {
	let cuerpo = null;
	try {
		cuerpo = await res.json();
	} catch {
	}
	const mensaje = mensajeDeDetalle(cuerpo?.detail) || mensajeDeDetalle(cuerpo?.error) || mensajeDeDetalle(cuerpo?.message);
	if (mensaje) return mensaje;
	return `Error ${res.status}: no se pudo completar la operacion.`;
}

export async function request(path, { method = 'GET', body, form, base = 'fastapi' } = {}) {
	const prefijo = PREFIJOS[base] ?? BASE_FASTAPI;
	const url = prefijo + path;

	const headers = ({});
	let payload;
	if (form) {
		headers['Content-Type'] = 'application/x-www-form-urlencoded';
		payload = new URLSearchParams(form).toString();
	} else if (body !== undefined) {
		headers['Content-Type'] = 'application/json';
		payload = JSON.stringify(body);
	}
	if (base === 'fastapi' && session.token) {
		headers.Authorization = `Bearer ${session.token}`;
	}

	let res;
	try {
		res = await fetch(url, { method, headers, body: payload });
	} catch {
		throw new Error('No se pudo conectar con el servidor. Verifica que la API este encendida.');
	}

	if (res.status === 401 && base === 'fastapi' && session.token) {
		cerrarSesion();
		goto('/login');
		throw new Error('Tu sesion expiro. Inicia sesion de nuevo.');
	}

	if (!res.ok) {
		throw new Error(await mensajeDeError(res));
	}

	if (res.status === 204) return null;
	const texto = await res.text();
	if (!texto) return null;
	try {
		return JSON.parse(texto);
	} catch {
		return texto;
	}
}
