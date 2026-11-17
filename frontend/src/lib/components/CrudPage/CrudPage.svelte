<script>
	import { onMount } from 'svelte';
	import { MODULOS, LOOKUPS } from '#lib/config/modulos.js';
	import { serviciosPorModulo } from '#lib/services/index.js';
	import { session, permisosDe } from '#lib/stores/session.svelte.js';
	import { exito, fallo } from '#lib/stores/toast.svelte.js';
	import { esc, badgeHtml, fechaHora, fecha, numero, aInputFechaHora } from '#lib/utils/formato.js';
	import PageHeader from '#lib/components/PageHeader/PageHeader.svelte';
	import DataTable from '#lib/components/DataTable/DataTable.svelte';
	import Modal from '#lib/components/Modal/Modal.svelte';
	import FormField from '#lib/components/FormField/FormField.svelte';
	import ConfirmDialog from '#lib/components/ConfirmDialog/ConfirmDialog.svelte';
	import LoadingSpinner from '#lib/components/LoadingSpinner/LoadingSpinner.svelte';
	import AlertBox from '#lib/components/AlertBox/AlertBox.svelte';

	let { modulo } = $props();

	const cfg = $derived(MODULOS[modulo]);
	const servicio = $derived(serviciosPorModulo[modulo]);
	const permisos = $derived(permisosDe(modulo));

	let datos = $state([]);
	let mapas = $state({});
	let listas = $state({});
	let cargando = $state(true);
	let error = $state('');

	let modalAbierto = $state(false);
	let editando = $state(null);
	let form = $state({});
	let guardando = $state(false);
	let errorForm = $state('');
	let aEliminar = $state(null);
	let eliminando = $state(false);

	const nombresLookup = $derived([
		...new Set(
			[...cfg.columnas, ...cfg.campos].map((x) => x.lookup).filter((x) => x !== undefined)
		)
	]);

	const aliasDe = (key) => (key.endsWith('_id') ? `${key.slice(0, -3)}_nombre` : null);

	const idDe = (fila) => fila[cfg.claveId ?? 'id'];

	const etiquetaDe = (fila, label) => {
		const valor = fila[label] ?? fila[`${label}_nombre`] ?? fila.nombre ?? fila.rol_nombre ?? fila.ubicacion;
		return valor === null || valor === undefined ? '' : String(valor);
	};

	async function cargarLookup(nombre) {
		const l = LOOKUPS[nombre];
		try {
			const filas = await serviciosPorModulo[l.servicio].listar();
			return [
				nombre,
				filas.map((r) => ({ valor: r.id, etiqueta: etiquetaDe(r, l.label) }))
			];
		} catch {
			return [nombre, []];
		}
	}

	async function cargar() {
		cargando = true;
		error = '';
		try {
			const [filas, ...lookups] = await Promise.all([
				servicio.listar(),
				...nombresLookup.map(cargarLookup)
			]);
			datos = filas;
			const nuevasListas = {};
			const nuevosMapas = {};
			for (const [nombre, lista] of lookups) {
				nuevasListas[nombre] = lista;
				nuevosMapas[nombre] = Object.fromEntries(lista.map((o) => [o.valor, o.etiqueta]));
			}
			listas = nuevasListas;
			mapas = nuevosMapas;
		} catch (e) {
			error = e instanceof Error ? e.message : String(e);
		} finally {
			cargando = false;
		}
	}

	onMount(cargar);

	const columnas = $derived(
		cfg.columnas.filter((c) => {
			if (!c.lookup) return true;
			const alias = aliasDe(c.key);
			if (alias && datos.some((f) => f[alias] !== undefined && f[alias] !== null && f[alias] !== '')) {
				return true;
			}
			return Object.keys(mapas[c.lookup] ?? {}).length > 0;
		})
	);

	function valorCelda(col, fila) {
		let v = fila[col.key];
		if (col.lookup) {
			const alias = aliasDe(col.key);
			const porAlias = alias ? fila[alias] : null;
			v =
				porAlias !== undefined && porAlias !== null && porAlias !== ''
					? porAlias
					: (mapas[col.lookup]?.[v] ?? '');
		}
		return v;
	}

	const filas = $derived(
		datos.map((original) => {
			const vista = {};
			const orden = {};
			for (const c of columnas) {
				const v = valorCelda(c, original);
				orden[c.key] = c.tipo === 'numero' ? (v === null || v === '' ? null : Number(v)) : (v ?? '');
				if (v === null || v === undefined || v === '') vista[c.key] = '<span class="text-muted">—</span>';
				else if (c.tipo === 'etiqueta') vista[c.key] = badgeHtml(v);
				else if (c.tipo === 'fechahora') vista[c.key] = esc(fechaHora(v));
				else if (c.tipo === 'fecha') vista[c.key] = esc(fecha(v));
				else if (c.tipo === 'numero') vista[c.key] = esc(numero(v));
				else vista[c.key] = esc(v);
			}
			return { original, vista, orden };
		})
	);

	const opcionesDe = (campo) =>
		campo.lookup
			? (listas[campo.lookup] ?? [])
			: (campo.opciones ?? []).map((o) => ({ valor: o, etiqueta: o }));

	const camposVisibles = $derived(cfg.campos.filter((c) => !(editando && c.soloCrear)));
	const esRequerido = (c) => !!(c.requerido || (c.requeridoAlCrear && !editando));

	function abrirCrear() {
		editando = null;
		form = Object.fromEntries(cfg.campos.map((c) => [c.key, '']));
		errorForm = '';
		modalAbierto = true;
	}

	function abrirEditar(fila) {
		editando = fila;
		form = Object.fromEntries(
			cfg.campos.map((c) => {
				let v = fila[c.key];
				if (c.tipo === 'date') v = v ? String(v).slice(0, 10) : '';
				else if (c.tipo === 'datetime-local') v = aInputFechaHora(v);
				else if (c.tipo === 'password') v = '';
				return [c.key, v ?? ''];
			})
		);
		errorForm = '';
		modalAbierto = true;
	}

	function armarPayload() {
		const payload = {};
		for (const c of camposVisibles) {
			let v = form[c.key];
			const vacio = v === '' || v === null || v === undefined;
			if (vacio) continue;
			if (c.tipo === 'number' || (c.tipo === 'select' && c.lookup)) v = Number(v);
			if (c.tipo === 'datetime-local') v = String(v).replace('T', ' ') + ':00';
			payload[c.key] = v;
		}
		if (!editando) {
			for (const [campo, origen] of Object.entries(cfg.automaticos ?? {})) {
				payload[campo] = (session)[origen];
			}
		}
		return payload;
	}

	async function guardar(e) {
		e.preventDefault();
		guardando = true;
		errorForm = '';
		try {
			const payload = armarPayload();
			if (editando) {
				await servicio.actualizar(idDe(editando), payload);
				exito(`${cfg.singular[0].toUpperCase() + cfg.singular.slice(1)} actualizado correctamente`);
			} else {
				await servicio.crear(payload);
				exito(`${cfg.singular[0].toUpperCase() + cfg.singular.slice(1)} registrado correctamente`);
			}
			modalAbierto = false;
			await cargar();
		} catch (err) {
			errorForm = err instanceof Error ? err.message : String(err);
		} finally {
			guardando = false;
		}
	}

	async function eliminar() {
		eliminando = true;
		try {
			await servicio.eliminar(idDe(aEliminar));
			exito('Registro eliminado');
			aEliminar = null;
			await cargar();
		} catch (err) {
			fallo(err instanceof Error ? err.message : String(err));
		} finally {
			eliminando = false;
		}
	}
</script>

<PageHeader titulo={cfg.titulo} icono={cfg.icono} subtitulo="Gestion de {cfg.titulo.toLowerCase()}">
	{#if permisos?.puede_crear}
		<button class="btn btn-primary" onclick={abrirCrear}>
			<i class="bi bi-plus-lg me-1"></i>Nuevo {cfg.singular}
		</button>
	{/if}
</PageHeader>

{#if !permisos}
	<AlertBox tipo="warning">Tu rol no tiene acceso a este modulo.</AlertBox>
{:else if cargando}
	<LoadingSpinner />
{:else if error}
	<AlertBox>{error}</AlertBox>
{:else}
	<div class="card">
		<div class="card-body">
			<DataTable
				{columnas}
				{filas}
				puedeEditar={permisos.puede_editar}
				puedeEliminar={permisos.puede_eliminar}
				onedit={abrirEditar}
				ondelete={(fila) => (aEliminar = fila)}
			/>
		</div>
	</div>
{/if}

<Modal
	titulo={editando ? `Editar ${cfg.singular}` : `Nuevo ${cfg.singular}`}
	abierto={modalAbierto}
	onclose={() => (modalAbierto = false)}
>
	<form id="form-crud" class="row g-3" onsubmit={guardar}>
		{#each camposVisibles as campo (campo.key)}
			<FormField
				{campo}
				bind:valor={form[campo.key]}
				opciones={opcionesDe(campo)}
				requerido={esRequerido(campo)}
			/>
		{/each}
		{#if errorForm}
			<div class="col-12"><AlertBox>{errorForm}</AlertBox></div>
		{/if}
	</form>
	{#snippet pie()}
		<button class="btn btn-outline-secondary" onclick={() => (modalAbierto = false)} disabled={guardando}>
			Cancelar
		</button>
		<button class="btn btn-primary" type="submit" form="form-crud" disabled={guardando}>
			{#if guardando}<span class="spinner-border spinner-border-sm me-1"></span>{/if}Guardar
		</button>
	{/snippet}
</Modal>

<ConfirmDialog
	abierto={!!aEliminar}
	mensaje="¿Seguro que deseas eliminar este {cfg.singular}? Dejara de mostrarse en el sistema."
	ocupado={eliminando}
	onconfirm={eliminar}
	oncancel={() => (aEliminar = null)}
/>
