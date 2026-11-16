// Mensajes emergentes (exito / error) compartidos por toda la aplicacion.
/**
 * @typedef {Object} Toast
 * @property {number} id
 * @property {string} mensaje
 * @property {string} tipo
 */

/** @type {Toast[]} */
export const toasts = $state([]);
let contador = 0;

/** @param {string} mensaje @param {string} tipo @param {number} ms */
export function notificar(mensaje, tipo = 'success', ms = 4000) {
	const id = ++contador;
	toasts.push({ id, mensaje, tipo });
	setTimeout(() => {
		const i = toasts.findIndex((t) => t.id === id);
		if (i >= 0) toasts.splice(i, 1);
	}, ms);
}

/** @param {string} m */
export const exito = (m) => notificar(m, 'success');
/** @param {string} m */
export const fallo = (m) => notificar(m, 'danger', 6000);
