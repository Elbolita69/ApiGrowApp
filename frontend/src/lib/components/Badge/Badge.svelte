<script>
	import { colorDe } from '#lib/utils/formato.js';

	let { texto } = $props();
</script>

<span class="badge text-bg-{colorDe(texto)}">{texto}</span>
