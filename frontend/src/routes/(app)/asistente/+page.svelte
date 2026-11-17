<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { preguntar } from '#lib/services/asistente.js';
	import { session } from '#lib/stores/session.svelte.js';
	import Header from '#lib/components/Header/Header.svelte';
	import Card from '#lib/components/Card/Card.svelte';
	import AlertBox from '#lib/components/AlertBox/AlertBox.svelte';
	import Badge from '#lib/components/Badge/Badge.svelte';
	import LoadingSpinner from '#lib/components/LoadingSpinner/LoadingSpinner.svelte';

	let pregunta = $state('');
	let respuesta = $state('');
	let error = $state('');
	let cargando = $state(false);
	let historial = $state([]);

	const EJEMPLOS = [
		'Cuantos invernaderos estan activos?',
		'Que sensores tienen la temperatura mas alta?',
		'Cuantas alertas hay pendientes?'
	];

	onMount(() => {
		if (!session.token) goto('/login', { replaceState: true });
		pregunta = '';
		respuesta = '';
		historial = [];
	});

	async function consultar(e) {
		e.preventDefault();
		const texto = pregunta.trim();
		if (!texto) {
			error = 'Escribe una pregunta para consultar al asistente.';
			return;
		}
		error = '';
		cargando = true;
		try {
			const r = await preguntar(texto);
			respuesta = r?.respuesta ?? '';
			historial = [{ pregunta: texto, respuesta: respuesta }, ...historial];
			pregunta = '';
		} catch (err) {
			error = err instanceof Error ? err.message : String(err);
		} finally {
			cargando = false;
		}
	}

	function usarEjemplo(texto) {
		pregunta = texto;
	}
</script>

<Header
	titulo="Asistente del invernadero"
	icono="bi-stars"
	subtitulo="Pregunta en lenguaje natural sobre los datos del sistema"
>
	<Badge texto="Respuesta en lenguaje natural" />
</Header>

<div class="row g-3">
	<div class="col-12 col-lg-7">
		<Card titulo="Nueva consulta" icono="bi-chat-left-text">
			<form onsubmit={consultar}>
				<div class="mb-3">
					<label class="form-label small fw-semibold" for="pregunta">Tu pregunta</label>
					<textarea
						id="pregunta"
						class="form-control"
						rows="3"
						bind:value={pregunta}
						placeholder="Ej.: cuantos cultivos hay en el invernadero principal?"
						required
					></textarea>
					<div class="form-text">El asistente responde con los datos del sistema, nunca con codigo SQL.</div>
				</div>
				<div class="d-flex flex-wrap gap-2 align-items-center">
					<button class="btn btn-primary" type="submit" disabled={cargando}>
						{#if cargando}
							<span class="spinner-border spinner-border-sm me-1"></span>Consultando...
						{:else}
							<i class="bi bi-send me-1"></i>Consultar
						{/if}
					</button>
					{#if cargando}<LoadingSpinner texto="Consultando la base de datos..." />{/if}
				</div>
			</form>

			{#if error}
				<div class="mt-3"><AlertBox>{error}</AlertBox></div>
			{/if}

			{#if respuesta}
				<div class="mt-3">
					<AlertBox tipo="info">{respuesta}</AlertBox>
				</div>
			{/if}
		</Card>
	</div>

	<div class="col-12 col-lg-5">
		<Card titulo="Ejemplos de preguntas" icono="bi-lightbulb">
			<div class="d-flex flex-column gap-2">
				{#each EJEMPLOS as ejemplo (ejemplo)}
					<button
						type="button"
						class="btn btn-outline-primary btn-sm text-start"
						onclick={() => usarEjemplo(ejemplo)}
					>
						<i class="bi bi-question-circle me-1"></i>{ejemplo}
					</button>
				{/each}
			</div>
		</Card>

		{#if historial.length}
			<div class="mt-3">
				<Card titulo="Consultas anteriores" icono="bi-clock-history">
					<ul class="list-group list-group-flush">
						{#each historial as item, i (i)}
							<li class="list-group-item px-0">
								<div class="fw-semibold small">{item.pregunta}</div>
								<div class="text-muted small">{item.respuesta}</div>
							</li>
						{/each}
					</ul>
				</Card>
			</div>
		{/if}
	</div>
</div>
