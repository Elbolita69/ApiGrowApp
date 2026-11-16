<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { restaurarSesion } from '#lib/stores/session.svelte.js';

	// La raiz solo redirige: al tablero si hay sesion, al login si no.
	onMount(() => goto(restaurarSesion() ? '/inicio' : '/login', { replaceState: true }));
</script>
