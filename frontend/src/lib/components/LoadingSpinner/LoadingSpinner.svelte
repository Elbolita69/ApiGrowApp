<script>
	let { texto = 'Cargando...' } = $props();
</script>

<div class="d-flex align-items-center justify-content-center gap-2 py-5 text-muted">
	<div class="spinner-border spinner-border-sm text-success" role="status"></div>
	<span>{texto}</span>
</div>
