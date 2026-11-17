import adapter from '@sveltejs/adapter-static';

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
