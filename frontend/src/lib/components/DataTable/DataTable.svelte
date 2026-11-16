<script>
	import DataTable from 'datatables.net-bs5';
	import 'datatables.net-bs5/css/dataTables.bootstrap5.min.css';

	/**
	 * Tabla con la libreria DataTables (busqueda, orden y paginacion).
	 * filas: [{ original, vista: {col: html}, orden: {col: valor} }]
	 * El ID del registro NUNCA se muestra: las acciones usan la fila original por posicion.
	 * @type {{columnas: Array<{key: string, label: string}>, filas: any[], puedeEditar?: boolean, puedeEliminar?: boolean, onedit?: (fila: any) => void, ondelete?: (fila: any) => void}}
	 */
	let { columnas, filas, puedeEditar = false, puedeEliminar = false, onedit, ondelete } = $props();

	/** @type {HTMLDivElement} */
	let host;

	const ES = {
		search: 'Buscar:',
		lengthMenu: 'Mostrar _MENU_ registros',
		info: 'Mostrando _START_ a _END_ de _TOTAL_ registros',
		infoEmpty: 'Sin registros para mostrar',
		infoFiltered: '(filtrado de _MAX_ registros)',
		emptyTable: 'No hay registros todavia',
		zeroRecords: 'No se encontraron coincidencias',
		paginate: { first: 'Primero', last: 'Ultimo', next: 'Siguiente', previous: 'Anterior' }
	};

	$effect(() => {
		const cols = columnas;
		const datos = filas;
		const editar = puedeEditar;
		const eliminar = puedeEliminar;

		const el = document.createElement('table');
		el.className = 'table table-hover align-middle w-100';
		host.appendChild(el);

		const columnasDt = /** @type {any[]} */ (
			cols.map((c) => ({
				title: c.label,
				// display: HTML (etiquetas); orden/busqueda: valor plano
				data: (/** @type {any} */ fila, /** @type {string} */ tipo) =>
					tipo === 'display' ? fila.vista[c.key] : fila.orden[c.key],
				defaultContent: ''
			}))
		);
		if (editar || eliminar) {
			columnasDt.push({
				title: 'Acciones',
				data: null,
				orderable: false,
				searchable: false,
				className: 'text-nowrap',
				render: (/** @type {any} */ d, /** @type {any} */ t, /** @type {any} */ fila, /** @type {any} */ meta) =>
					(editar
						? `<button class="btn btn-sm btn-outline-primary me-1" data-act="edit" data-i="${meta.row}" title="Editar"><i class="bi bi-pencil-square"></i></button>`
						: '') +
					(eliminar
						? `<button class="btn btn-sm btn-outline-danger" data-act="del" data-i="${meta.row}" title="Eliminar"><i class="bi bi-trash"></i></button>`
						: '')
			});
		}

		const tabla = new DataTable(el, {
			data: datos,
			columns: columnasDt,
			language: ES,
			pageLength: 10,
			order: []
		});

		return () => {
			tabla.destroy();
			host.innerHTML = '';
		};
	});

	/** @param {MouseEvent} e */
	function clic(e) {
		const boton = /** @type {HTMLButtonElement | null} */ (
			/** @type {HTMLElement | null} */ (e.target)?.closest('button[data-act]')
		);
		if (!boton) return;
		const fila = filas[Number(boton.dataset.i)];
		if (!fila) return;
		if (boton.dataset.act === 'edit') onedit?.(fila.original);
		else ondelete?.(fila.original);
	}
</script>

<!-- svelte-ignore a11y_click_events_have_key_events, a11y_no_static_element_interactions -->
<div class="table-responsive" bind:this={host} onclick={clic}></div>
