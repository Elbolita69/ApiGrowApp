# Arranca la API auxiliar (Express + MySQL) en Windows. Opcional.
# Uso: powershell -ExecutionPolicy Bypass -File scripts\iniciar_api_express.ps1

$ErrorActionPreference = "Stop"
$raiz = Split-Path -Parent $PSScriptRoot
Set-Location (Join-Path $raiz "express-api")

if (-not (Test-Path "node_modules")) {
    Write-Host "Faltan las dependencias. Ejecuta primero scripts\instalar_dependencias.ps1" -ForegroundColor Red
    exit 1
}

npm start
