<script>
	/**
	 * Ventana modal reutilizable.
	 * @type {{titulo: string, abierto: boolean, onclose: () => void, tamano?: string, children: import('svelte').Snippet, pie?: import('svelte').Snippet}}
	 */
	let { titulo, abierto, onclose, tamano = 'lg', children, pie } = $props();

	/** @param {KeyboardEvent} e */
	function teclado(e) {
		if (abierto && e.key === 'Escape') onclose();
	}
</script>

<svelte:window onkeydown={teclado} />

{#if abierto}
	<div class="modal d-block" tabindex="-1" style="background: rgba(0,0,0,.5)" role="dialog" aria-modal="true">
		<div class="modal-dialog modal-{tamano} modal-dialog-scrollable modal-dialog-centered">
			<div class="modal-content border-0 shadow">
				<div class="modal-header" style="background: var(--grow-soft)">
					<h2 class="modal-title h5 mb-0" style="color: var(--grow-dark)">{titulo}</h2>
					<button type="button" class="btn-close" aria-label="Cerrar" onclick={onclose}></button>
				</div>
				<div class="modal-body">{@render children()}</div>
				{#if pie}<div class="modal-footer">{@render pie()}</div>{/if}
			</div>
		</div>
	</div>
{/if}
