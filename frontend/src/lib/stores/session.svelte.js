// Sesion del usuario: token JWT, datos del usuario y modulos permitidos para su rol.
// Los modulos vienen de la base de datos (tabla moduloxrol) a traves de GET /auth/modulos.
const KEY = 'growapp_token';

/**
 * Permisos de un modulo para el rol del usuario (tabla moduloxrol).
 * @typedef {Object} Modulo
 * @property {string} nombre
 * @property {string} descripcion
 * @property {boolean} puede_ver
 * @property {boolean} puede_crear
 * @property {boolean} puede_editar
 * @property {boolean} puede_eliminar
 */

/**
 * @typedef {Object} Claims
 * @property {number} sub
 * @property {string} username
 * @property {string} rol
 */

/** @returns {string|null} */
function leerToken() {
	try {
		return localStorage.getItem(KEY);
	} catch {
		return null;
	}
}

/** @param {string} token @returns {Claims|null} */
function decodificar(token) {
	try {
		const payload = token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/');
		return JSON.parse(decodeURIComponent(escape(atob(payload))));
	} catch {
		return null;
	}
}

/**
 * @type {{
 *   token: string | null,
 *   userId: number | null,
 *   username: string,
 *   rol: string,
 *   nombre: string,
 *   modulos: Modulo[],
 *   listo: boolean
 * }}
 */
export const session = $state({
	token: null,
	userId: null,
	username: '',
	rol: '',
	nombre: '',
	modulos: [],
	listo: false
});

/** @param {string} token */
export function iniciarSesion(token) {
	const data = decodificar(token);
	session.token = token;
	session.userId = data ? Number(data.sub) : null;
	session.username = data?.username ?? '';
	session.rol = data?.rol ?? '';
	try {
		localStorage.setItem(KEY, token);
	} catch {
		/* almacenamiento no disponible */
	}
}

export function restaurarSesion() {
	const token = leerToken();
	if (token) iniciarSesion(token);
	return !!token;
}

export function cerrarSesion() {
	session.token = null;
	session.userId = null;
	session.username = '';
	session.rol = '';
	session.nombre = '';
	session.modulos = [];
	session.listo = false;
	try {
		localStorage.removeItem(KEY);
	} catch {
		/* almacenamiento no disponible */
	}
}

/** Permisos del usuario sobre un modulo (null si el rol no tiene acceso). */
/** @param {string} nombreModulo @returns {Modulo|null} */
export function permisosDe(nombreModulo) {
	return session.modulos.find((m) => m.nombre === nombreModulo) ?? null;
}
