import adapter from '@sveltejs/adapter-static';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [
		sveltekit({
			compilerOptions: {
				// Force runes mode for the project, except for libraries. Can be removed in svelte 6.
				runes: ({ filename }) =>
					filename.split(/[/\\]/).includes('node_modules') ? undefined : true
			},

			// Aplicacion de una sola pagina (SPA): se publica como sitio estatico en Render.
			// El fallback index.html permite recargar cualquier ruta (/cultivos, /usuarios...).
			adapter: adapter({ fallback: 'index.html' })
		})
	]
});
