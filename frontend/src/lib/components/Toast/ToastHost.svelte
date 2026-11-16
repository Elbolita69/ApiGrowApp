<script>
	import { toasts } from '#lib/stores/toast.svelte.js';
</script>

<div class="toast-container position-fixed top-0 end-0 p-3" style="z-index: 2000">
	{#each toasts as t (t.id)}
		<div class="toast show align-items-center text-bg-{t.tipo} border-0 mb-2" role="alert">
			<div class="d-flex">
				<div class="toast-body">{t.mensaje}</div>
			</div>
		</div>
	{/each}
</div>
