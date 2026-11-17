<script>
	import PageHeader from '#lib/components/PageHeader/PageHeader.svelte';

	let { titulo, subtitulo = '', icono = 'bi-grid', children } = $props();
</script>

<PageHeader {titulo} {subtitulo} {icono}>
	{@render children?.()}
</PageHeader>
