<script>
	/** @type {{tipo?: string, children: import('svelte').Snippet}} */
	let { tipo = 'danger', children } = $props();
</script>

<div class="alert alert-{tipo} d-flex align-items-start gap-2" role="alert">
	<i class="bi bi-exclamation-triangle-fill"></i>
	<div>{@render children()}</div>
</div>
