<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { restaurarSesion } from '#lib/stores/session.svelte.js';

	onMount(() => goto(restaurarSesion() ? '/inicio' : '/login', { replaceState: true }));
</script>
