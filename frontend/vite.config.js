import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

const API_TARGET = process.env.VITE_API_TARGET || 'http://localhost:8000';
const EXPRESS_TARGET = process.env.VITE_EXPRESS_TARGET || 'http://localhost:3000';

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		proxy: {
			'/api-express': {
				target: EXPRESS_TARGET,
				changeOrigin: true,
				rewrite: (path) => path.replace(/^\/api-express/, '')
			},
			'/api': {
				target: API_TARGET,
				changeOrigin: true,
				rewrite: (path) => path.replace(/^\/api/, '')
			}
		}
	}
});
