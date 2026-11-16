<script>
	/** @type {{tipo?: string, children: import('svelte').Snippet}} */
	let { tipo = 'danger', children } = $props();

	// Icono segun el tipo de aviso.
	/** @type {Record<string, string>} */
	const ICONOS = {
		danger: 'bi-exclamation-triangle-fill',
		warning: 'bi-exclamation-triangle-fill',
		success: 'bi-check-circle-fill',
		info: 'bi-info-circle-fill',
		primary: 'bi-info-circle-fill'
	};
	const icono = $derived(ICONOS[tipo] ?? ICONOS.danger);
</script>

<div class="alert alert-{tipo} d-flex align-items-start gap-2" role="alert">
	<i class="bi {icono}"></i>
	<div>{@render children()}</div>
</div>
