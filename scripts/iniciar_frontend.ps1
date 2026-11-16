# Arranca el frontend (SvelteKit) en Windows.
# Uso: powershell -ExecutionPolicy Bypass -File scripts\iniciar_frontend.ps1

$ErrorActionPreference = "Stop"
$raiz = Split-Path -Parent $PSScriptRoot
Set-Location (Join-Path $raiz "frontend")

if (-not (Test-Path "node_modules")) {
    Write-Host "Faltan las dependencias. Ejecuta primero scripts\instalar_dependencias.ps1" -ForegroundColor Red
    exit 1
}

npm run dev
