<script>
	/**
	 * Tarjeta reutilizable: titulo, icono y espacio para el contenido (y un pie opcional).
	 * @type {{titulo?: string, subtitulo?: string, icono?: string, children?: import('svelte').Snippet, pie?: import('svelte').Snippet}}
	 */
	let { titulo = '', subtitulo = '', icono = '', children, pie } = $props();
</script>

<div class="card h-100">
	{#if titulo}
		<div class="card-header bg-white d-flex align-items-center gap-2">
			{#if icono}
				<i class="bi {icono} fs-5" style="color: var(--grow-primary)"></i>
			{/if}
			<div class="min-w-0">
				<div class="fw-semibold text-truncate" style="color: var(--grow-dark)">{titulo}</div>
				{#if subtitulo}<small class="text-muted">{subtitulo}</small>{/if}
			</div>
		</div>
	{/if}
	<div class="card-body">{@render children?.()}</div>
	{#if pie}<div class="card-footer bg-white">{@render pie()}</div>{/if}
</div>
