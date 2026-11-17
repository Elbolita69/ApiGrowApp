<script>
	import '../app.css';
	import favicon from '#lib/assets/favicon.svg';
	import ToastHost from '#lib/components/Toast/ToastHost.svelte';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

{@render children()}
<ToastHost />
