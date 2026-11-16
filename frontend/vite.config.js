import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

// Se pueden cambiar sin tocar codigo (variables de entorno del proceso de Vite).
const API_TARGET = process.env.VITE_API_TARGET || 'http://localhost:8000';
const EXPRESS_TARGET = process.env.VITE_EXPRESS_TARGET || 'http://localhost:3000';

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		proxy: {
			// Ojo: '/api-express' va ANTES de '/api' porque '/api-express' tambien
			// empieza por '/api' y el primero que coincide gana.
			'/api-express': {
				target: EXPRESS_TARGET,
				changeOrigin: true,
				rewrite: (path) => path.replace(/^\/api-express/, '')
			},
			'/api': {
				target: API_TARGET,
				changeOrigin: true,
				// La API expone /auth/login, no /api/auth/login: se quita el prefijo.
				rewrite: (path) => path.replace(/^\/api/, '')
			}
		}
	}
});
