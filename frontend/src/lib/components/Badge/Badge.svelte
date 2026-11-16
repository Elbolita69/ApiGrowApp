<script>
	import { colorDe } from '#lib/utils/formato.js';

	/** Etiqueta de color segun el texto (prioridades, estados, roles...). */
	let { texto } = $props();
</script>

<span class="badge text-bg-{colorDe(texto)}">{texto}</span>
