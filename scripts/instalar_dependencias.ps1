# Instalacion de dependencias en Windows (PowerShell).
# Uso: powershell -ExecutionPolicy Bypass -File scripts\instalar_dependencias.ps1

$ErrorActionPreference = "Stop"
$raiz = Split-Path -Parent $PSScriptRoot
Set-Location $raiz

Write-Host "== Python ==" -ForegroundColor Green
if (-not (Test-Path ".venv")) {
    python -m venv .venv
    Write-Host "Entorno virtual .venv creado."
} else {
    Write-Host "El entorno virtual .venv ya existe."
}
& ".venv\Scripts\python.exe" -m pip install --upgrade pip
& ".venv\Scripts\python.exe" -m pip install -r requirements.txt

Write-Host "== Frontend (SvelteKit) ==" -ForegroundColor Green
Set-Location "frontend"
npm install
Set-Location $raiz

Write-Host "== API auxiliar (Express + MySQL, opcional) ==" -ForegroundColor Green
Set-Location "express-api"
npm install
Set-Location $raiz

Write-Host ""
Write-Host "Listo. Copia .env.example a .env y completa las credenciales." -ForegroundColor Cyan
