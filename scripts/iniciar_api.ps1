# Arranca la API principal (FastAPI + PostgreSQL) en Windows.
# Uso: powershell -ExecutionPolicy Bypass -File scripts\iniciar_api.ps1

$ErrorActionPreference = "Stop"
$raiz = Split-Path -Parent $PSScriptRoot
Set-Location $raiz

$python = Join-Path $raiz ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    Write-Host "No existe .venv. Ejecuta primero scripts\instalar_dependencias.ps1" -ForegroundColor Red
    exit 1
}
if (-not (Test-Path ".env")) {
    Write-Host "Falta el archivo .env. Copia .env.example a .env y completa los datos." -ForegroundColor Red
    exit 1
}

& $python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
