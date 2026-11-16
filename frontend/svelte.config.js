import adapter from '@sveltejs/adapter-static';

/**
 * Configuracion de SvelteKit (la que faltaba al venir de macOS).
 *
 * - adapter-static con fallback 'index.html': la app es una SPA y cualquier ruta
 *   (/cultivos, /usuarios, /asistente...) se puede recargar sin error 404.
 * - compilerOptions.runes = true: Svelte 5 en modo runes para todo el proyecto.
 *
 * El SSR y el prerender se desactivan por pagina en `src/routes/+layout.js`
 * (export const ssr = false; export const prerender = false); se declaran aqui
 * para dejar la intencion a la vista.
 */
export const ssr = false;
export const prerender = false;

export default {
	compilerOptions: {
		runes: true
	},
	kit: {
		adapter: adapter({ fallback: 'index.html' })
	}
};
