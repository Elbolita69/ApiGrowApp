<script>
	import { page } from '$app/state';

	/**
	 * items: [{ ruta, titulo, icono }] construidos con los modulos del rol (tabla moduloxrol).
	 * @type {{items: Array<{ruta: string, titulo: string, icono: string}>, abierto: boolean, oncerrar: () => void}}
	 */
	let { items, abierto, oncerrar } = $props();
</script>

{#if abierto}
	<!-- svelte-ignore a11y_click_events_have_key_events, a11y_no_static_element_interactions -->
	<div class="sidebar-backdrop d-lg-none" onclick={oncerrar}></div>
{/if}

<aside class="sidebar bg-white shadow-sm" class:abierto>
	<ul class="nav nav-pills flex-column gap-1 p-3">
		<li class="nav-item">
			<a
				class="nav-link"
				class:active={page.url.pathname === '/inicio'}
				href="/inicio"
				onclick={oncerrar}
			>
				<i class="bi bi-speedometer2 me-2"></i>Inicio
			</a>
		</li>
		{#each items as item (item.ruta)}
			<li class="nav-item">
				<a
					class="nav-link"
					class:active={page.url.pathname === item.ruta}
					href={item.ruta}
					onclick={oncerrar}
				>
					<i class="bi {item.icono} me-2"></i>{item.titulo}
				</a>
			</li>
		{/each}
	</ul>
</aside>

<style>
	.sidebar {
		width: 250px;
		min-height: calc(100vh - 56px);
		flex-shrink: 0;
	}
	.nav-link {
		color: #37474f;
		border-radius: 0.6rem;
	}
	.nav-link:hover {
		background: var(--grow-soft);
	}
	.nav-link.active {
		background: var(--grow-primary);
		color: #fff;
	}
	.sidebar-backdrop {
		position: fixed;
		inset: 56px 0 0 0;
		background: rgba(0, 0, 0, 0.4);
		z-index: 1030;
	}
	@media (max-width: 991.98px) {
		.sidebar {
			position: fixed;
			top: 56px;
			bottom: 0;
			left: -260px;
			z-index: 1040;
			transition: left 0.2s;
			overflow-y: auto;
		}
		.sidebar.abierto {
			left: 0;
		}
	}
</style>
