<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { auth } from '#lib/services/index.js';
	import { MODULOS } from '#lib/config/modulos.js';
	import { session, restaurarSesion, cerrarSesion } from '#lib/stores/session.svelte.js';
	import Navbar from '#lib/components/Navbar/Navbar.svelte';
	import Sidebar from '#lib/components/Sidebar/Sidebar.svelte';
	import Footer from '#lib/components/Footer/Footer.svelte';
	import LoadingSpinner from '#lib/components/LoadingSpinner/LoadingSpinner.svelte';

	let { children } = $props();
	let menuAbierto = $state(false);

	const items = $derived([
		...session.modulos
			.filter((m) => MODULOS[m.nombre])
			.map((m) => ({
				ruta: '/' + MODULOS[m.nombre].ruta,
				titulo: MODULOS[m.nombre].titulo,
				icono: MODULOS[m.nombre].icono
			})),
		{ ruta: '/asistente', titulo: 'Asistente', icono: 'bi-stars' }
	]);

	onMount(async () => {
		if (!session.token && !restaurarSesion()) {
			goto('/login', { replaceState: true });
			return;
		}
		try {
			const [modulos, yo] = await Promise.all([auth.modulos(), auth.me()]);
			session.modulos = modulos;
			session.nombre = yo.nombre || session.nombre;
			session.rol = yo.rol || session.rol;
			session.listo = true;
		} catch {
			cerrarSesion();
			goto('/login', { replaceState: true });
		}
	});

	function salir() {
		cerrarSesion();
		goto('/login');
	}
</script>

{#if session.listo}
	<Navbar usuario={session.nombre || session.username} rol={session.rol} onmenu={() => (menuAbierto = !menuAbierto)} onlogout={salir} />
	<div class="d-flex">
		<Sidebar {items} abierto={menuAbierto} oncerrar={() => (menuAbierto = false)} />
		<div class="flex-grow-1 min-vw-0 d-flex flex-column" style="min-width: 0">
			<main class="container-fluid p-3 p-md-4 flex-grow-1">
				{@render children()}
			</main>
			<Footer />
		</div>
	</div>
{:else}
	<LoadingSpinner texto="Verificando sesion..." />
{/if}
