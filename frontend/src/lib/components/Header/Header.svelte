<script>
	import PageHeader from '#lib/components/PageHeader/PageHeader.svelte';

	/**
	 * Encabezado de pagina: titulo, subtitulo, icono y espacio para acciones.
	 * Envuelve a PageHeader para no duplicar la logica del encabezado.
	 * @type {{titulo: string, subtitulo?: string, icono?: string, children?: import('svelte').Snippet}}
	 */
	let { titulo, subtitulo = '', icono = 'bi-grid', children } = $props();
</script>

<PageHeader {titulo} {subtitulo} {icono}>
	{@render children?.()}
</PageHeader>
