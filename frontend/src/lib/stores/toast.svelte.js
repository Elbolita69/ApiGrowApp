// Mensajes emergentes (exito / error) compartidos por toda la aplicacion.
export const toasts = $state([]);
let contador = 0;

export function notificar(mensaje, tipo = 'success', ms = 4000) {
	const id = ++contador;
	toasts.push({ id, mensaje, tipo });
	setTimeout(() => {
		const i = toasts.findIndex((t) => t.id === id);
		if (i >= 0) toasts.splice(i, 1);
	}, ms);
}

export const exito = (m) => notificar(m, 'success');
export const fallo = (m) => notificar(m, 'danger', 6000);
