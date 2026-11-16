<script>
	import { onMount } from 'svelte';
	import { serviciosPorModulo } from '#lib/services/index.js';
	import { MODULOS } from '#lib/config/modulos.js';
	import { session } from '#lib/stores/session.svelte.js';
	import { fechaHora } from '#lib/utils/formato.js';
	import PageHeader from '#lib/components/PageHeader/PageHeader.svelte';
	import StatCard from '#lib/components/StatCard/StatCard.svelte';
	import Badge from '#lib/components/Badge/Badge.svelte';
	import LoadingSpinner from '#lib/components/LoadingSpinner/LoadingSpinner.svelte';

	/** @type {Record<string, number | string>} */
	let conteos = $state({});
	/** @type {any[]} */
	let alertas = $state([]);
	let cargando = $state(true);

	const modulos = $derived(session.modulos.filter((m) => MODULOS[m.nombre]));
	const puedeVerAlertas = $derived(session.modulos.some((m) => m.nombre === 'alerts'));

	onMount(async () => {
		// Resumen en vivo: cada rol ve el numero de registros de SUS modulos
		// (los cambios hechos por otros roles se reflejan aqui).
		const resultados = await Promise.all(
			modulos.map(async (m) => {
				try {
					const filas = await serviciosPorModulo[m.nombre].listar();
					if (m.nombre === 'alerts') {
						alertas = filas.filter((/** @type {any} */ a) => a.estado_alerta !== 'resuelta').slice(0, 6);
					}
					return [m.nombre, filas.length];
				} catch {
					return [m.nombre, '-'];
				}
			})
		);
		conteos = Object.fromEntries(resultados);
		cargando = false;
	});
</script>

<PageHeader
	titulo="Hola, {session.nombre || session.username}"
	icono="bi-speedometer2"
	subtitulo="Resumen del sistema segun los modulos de tu rol"
>
	<Badge texto={session.rol} />
</PageHeader>

{#if cargando}
	<LoadingSpinner />
{:else}
	<div class="row g-3 mb-4">
		{#each modulos as m (m.nombre)}
			<div class="col-12 col-sm-6 col-xl-4">
				<StatCard
					titulo={MODULOS[m.nombre].titulo}
					valor={conteos[m.nombre]}
					icono={MODULOS[m.nombre].icono}
					href={'/' + MODULOS[m.nombre].ruta}
				/>
			</div>
		{/each}
	</div>

	{#if puedeVerAlertas}
		<div class="card">
			<div class="card-header bg-white fw-semibold">
				<i class="bi bi-bell me-1"></i>Alertas pendientes
			</div>
			<ul class="list-group list-group-flush">
				{#each alertas as a (a.id)}
					<li class="list-group-item d-flex justify-content-between align-items-center gap-2 flex-wrap">
						<div>
							<div>{a.mensaje}</div>
							<small class="text-muted">{a.greenhouse_nombre} · {fechaHora(a.creado)}</small>
						</div>
						<div class="d-flex gap-1"><Badge texto={a.prioridad} /><Badge texto={a.estado_alerta} /></div>
					</li>
				{:else}
					<li class="list-group-item text-muted">No hay alertas pendientes.</li>
				{/each}
			</ul>
		</div>
	{/if}
{/if}
