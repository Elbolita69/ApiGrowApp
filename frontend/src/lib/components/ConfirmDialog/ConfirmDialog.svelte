<script>
	import Modal from '#lib/components/Modal/Modal.svelte';

	/** @type {{abierto: boolean, mensaje: string, ocupado?: boolean, onconfirm: () => void, oncancel: () => void}} */
	let { abierto, mensaje, ocupado = false, onconfirm, oncancel } = $props();
</script>

<Modal titulo="Confirmar eliminacion" {abierto} onclose={oncancel} tamano="md">
	<p class="mb-0">{mensaje}</p>
	{#snippet pie()}
		<button class="btn btn-outline-secondary" onclick={oncancel} disabled={ocupado}>Cancelar</button>
		<button class="btn btn-danger" onclick={onconfirm} disabled={ocupado}>
			{#if ocupado}<span class="spinner-border spinner-border-sm me-1"></span>{/if}Eliminar
		</button>
	{/snippet}
</Modal>
