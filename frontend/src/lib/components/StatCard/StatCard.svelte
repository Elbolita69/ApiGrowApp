<script>
	let { titulo, valor, icono = 'bi-grid', href = '' } = $props();
</script>

<a class="text-decoration-none" {href}>
	<div class="card h-100 stat">
		<div class="card-body d-flex align-items-center gap-3">
			<div class="icono"><i class="bi {icono}"></i></div>
			<div>
				<div class="fs-4 fw-bold text-dark">{valor}</div>
				<div class="small text-muted">{titulo}</div>
			</div>
		</div>
	</div>
</a>

<style>
	.stat {
		transition: transform 0.15s;
	}
	.stat:hover {
		transform: translateY(-2px);
	}
	.icono {
		width: 48px;
		height: 48px;
		border-radius: 0.8rem;
		background: var(--grow-soft);
		color: var(--grow-primary);
		display: grid;
		place-items: center;
		font-size: 1.4rem;
	}
</style>
