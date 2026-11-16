<script>
	/**
	 * Campo de formulario reutilizable (texto, numero, fecha, lista desplegable, area de texto).
	 * Los selects reciben opciones [{valor, etiqueta}]: el usuario elige por nombre, nunca por ID.
	 * @type {{campo: any, valor: any, opciones?: Array<{valor: any, etiqueta: string}>, requerido?: boolean}}
	 */
	let { campo, valor = $bindable(), opciones = [], requerido = false } = $props();
	const id = 'campo_' + campo.key;
</script>

<div class="col-12 col-md-{campo.ancho ?? 6}">
	<label class="form-label small fw-semibold" for={id}>
		{campo.label}{#if requerido}<span class="text-danger"> *</span>{/if}
	</label>
	{#if campo.tipo === 'select'}
		<select class="form-select" {id} bind:value={valor} required={requerido}>
			<option value="">Selecciona...</option>
			{#each opciones as o (o.valor)}
				<option value={o.valor}>{o.etiqueta}</option>
			{/each}
		</select>
	{:else if campo.tipo === 'textarea'}
		<textarea class="form-control" {id} rows="3" bind:value={valor} required={requerido}></textarea>
	{:else}
		<input
			class="form-control"
			{id}
			type={campo.tipo}
			step={campo.step}
			min={campo.min}
			value={valor ?? ''}
			oninput={(e) => (valor = e.currentTarget.value)}
			required={requerido}
			autocomplete={campo.tipo === 'password' ? 'new-password' : 'off'}
		/>
	{/if}
	{#if campo.ayuda}<div class="form-text">{campo.ayuda}</div>{/if}
</div>
