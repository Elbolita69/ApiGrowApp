<script>
	/** @type {{titulo: string, icono?: string, subtitulo?: string, children?: import('svelte').Snippet}} */
	let { titulo, icono = 'bi-grid', subtitulo = '', children } = $props();
</script>

<div class="d-flex flex-wrap justify-content-between align-items-center gap-2 mb-3">
	<div>
		<h1 class="h4 mb-0" style="color: var(--grow-dark)">
			<i class="bi {icono} me-2"></i>{titulo}
		</h1>
		{#if subtitulo}<p class="text-muted small mb-0">{subtitulo}</p>{/if}
	</div>
	<div>{@render children?.()}</div>
</div>
