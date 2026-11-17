<script>
	import DataTable from 'datatables.net-bs5';
	import 'datatables.net-bs5/css/dataTables.bootstrap5.min.css';

	let { columnas, filas, puedeEditar = false, puedeEliminar = false, onedit, ondelete } = $props();

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

		const columnasDt = (
			cols.map((c) => ({
				title: c.label,
				data: (fila, tipo) =>
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
				render: (d, t, fila, meta) =>
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

	function clic(e) {
		const boton = (
			(e.target)?.closest('button[data-act]')
		);
		if (!boton) return;
		const fila = filas[Number(boton.dataset.i)];
		if (!fila) return;
		if (boton.dataset.act === 'edit') onedit?.(fila.original);
		else ondelete?.(fila.original);
	}
</script>

<div class="table-responsive" role="presentation" bind:this={host} onclick={clic}></div>
