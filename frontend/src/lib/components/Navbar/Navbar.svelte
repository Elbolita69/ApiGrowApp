<script>
	import Badge from '#lib/components/Badge/Badge.svelte';

	let { usuario, rol, onmenu, onlogout } = $props();
</script>

<nav class="navbar navbar-dark sticky-top shadow-sm" style="background: var(--grow-dark)">
	<div class="container-fluid">
		<div class="d-flex align-items-center gap-2">
			<button class="btn btn-outline-light btn-sm d-lg-none" onclick={onmenu} aria-label="Abrir menu">
				<i class="bi bi-list"></i>
			</button>
			<a class="navbar-brand fw-semibold mb-0" href="/inicio">
				<i class="bi bi-flower1 me-1" style="color: var(--grow-accent)"></i>GrowApp
			</a>
		</div>
		<div class="d-flex align-items-center gap-3 text-white">
			<span class="d-none d-sm-inline small">
				<i class="bi bi-person-circle me-1"></i>{usuario}
			</span>
			<Badge texto={rol} />
			<button class="btn btn-outline-light btn-sm" onclick={onlogout}>
				<i class="bi bi-box-arrow-right me-1"></i>Salir
			</button>
		</div>
	</div>
</nav>
