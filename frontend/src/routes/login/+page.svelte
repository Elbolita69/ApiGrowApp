<script>
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { login } from '#lib/services/auth.js';
	import { iniciarSesion, restaurarSesion } from '#lib/stores/session.svelte.js';
	import AlertBox from '#lib/components/AlertBox/AlertBox.svelte';

	let username = $state('');
	let password = $state('');
	let error = $state('');
	let cargando = $state(false);

	onMount(() => {
		if (restaurarSesion()) goto('/inicio', { replaceState: true });
	});

	async function entrar(e) {
		e.preventDefault();
		error = '';
		cargando = true;
		try {
			const r = await login(username, password);
			iniciarSesion(r.access_token);
			await goto('/inicio');
		} catch (err) {
			error = err instanceof Error ? err.message : String(err);
		} finally {
			cargando = false;
		}
	}
</script>

<div class="login min-vh-100 d-flex align-items-center justify-content-center p-3">
	<div class="card shadow-lg" style="max-width: 420px; width: 100%">
		<div class="card-body p-4 p-md-5">
			<div class="text-center mb-4">
				<i class="bi bi-flower1 display-4" style="color: var(--grow-primary)"></i>
				<h1 class="h3 mt-2 mb-0" style="color: var(--grow-dark)">GrowApp</h1>
				<p class="text-muted small">Invernadero inteligente</p>
			</div>
			<form onsubmit={entrar}>
				<div class="mb-3">
					<label class="form-label" for="usuario">Usuario</label>
					<div class="input-group">
						<span class="input-group-text"><i class="bi bi-person"></i></span>
						<input id="usuario" class="form-control" bind:value={username} required autocomplete="username" />
					</div>
				</div>
				<div class="mb-3">
					<label class="form-label" for="clave">Contrasena</label>
					<div class="input-group">
						<span class="input-group-text"><i class="bi bi-lock"></i></span>
						<input id="clave" type="password" class="form-control" bind:value={password} required autocomplete="current-password" />
					</div>
				</div>
				{#if error}<AlertBox>{error}</AlertBox>{/if}
				<button class="btn btn-primary w-100" disabled={cargando}>
					{#if cargando}<span class="spinner-border spinner-border-sm me-1"></span>{/if}Ingresar
				</button>
			</form>
		</div>
	</div>
</div>

<style>
	.login {
		background: linear-gradient(135deg, #1b5e20 0%, #43a047 55%, #aed581 100%);
	}
</style>
