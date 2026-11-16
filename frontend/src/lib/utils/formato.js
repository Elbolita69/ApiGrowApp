// Funciones de formato compartidas por la tabla, las etiquetas y el tablero.

export const COLORES = {
	alta: 'danger',
	media: 'warning',
	baja: 'secondary',
	activa: 'danger',
	reconocida: 'warning',
	resuelta: 'success',
	exitoso: 'success',
	parcial: 'warning',
	fallido: 'danger',
	activo: 'success',
	inactivo: 'secondary',
	creciendo: 'success',
	floracion: 'info',
	cosechado: 'primary',
	perdido: 'danger',
	administrador: 'warning',
	operador: 'info',
	agronomo: 'success',
	automatico: 'info',
	manual: 'secondary'
};

export const colorDe = (texto) => COLORES[String(texto).toLowerCase()] ?? 'secondary';

export function esc(valor) {
	return String(valor ?? '')
		.replace(/&/g, '&amp;')
		.replace(/</g, '&lt;')
		.replace(/>/g, '&gt;')
		.replace(/"/g, '&quot;')
		.replace(/'/g, '&#39;');
}

export const badgeHtml = (texto) => `<span class="badge text-bg-${colorDe(texto)}">${esc(texto)}</span>`;

export function fechaHora(v) {
	if (!v) return '';
	const d = new Date(v);
	return isNaN(d) ? String(v) : d.toLocaleString('es-CO', { dateStyle: 'short', timeStyle: 'short' });
}

export function fecha(v) {
	if (!v) return '';
	const [a, m, d] = String(v).slice(0, 10).split('-');
	return a && m && d ? `${d}/${m}/${a}` : String(v);
}

export const numero = (v) =>
	v === null || v === undefined || v === '' ? '' : new Intl.NumberFormat('es-CO', { maximumFractionDigits: 2 }).format(Number(v));

/** Convierte un valor ISO a 'YYYY-MM-DDTHH:mm' en hora local (para <input type="datetime-local">). */
export function aInputFechaHora(v) {
	if (!v) return '';
	const d = new Date(v);
	if (isNaN(d)) return '';
	const p = (n) => String(n).padStart(2, '0');
	return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}T${p(d.getHours())}:${p(d.getMinutes())}`;
}
