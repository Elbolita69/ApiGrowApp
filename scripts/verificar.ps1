# Diagnostico del proyecto en Windows.
# Comprueba paso a paso que todo este listo para arrancar.
# Uso: powershell -ExecutionPolicy Bypass -File scripts\verificar.ps1

$ErrorActionPreference = "Continue"
$raiz = Split-Path -Parent $PSScriptRoot
Set-Location $raiz

$fallos = 0

function Titulo($texto) {
    Write-Host ""
    Write-Host "== $texto ==" -ForegroundColor Cyan
}

function Ok($texto)    { Write-Host "  [OK]   $texto" -ForegroundColor Green }
function Aviso($texto) { Write-Host "  [--]   $texto" -ForegroundColor Yellow }
function Mal($texto)   { Write-Host "  [FALLA] $texto" -ForegroundColor Red; $script:fallos++ }

Titulo "Herramientas del sistema"
foreach ($cmd in @("python", "node", "npm")) {
    $encontrado = Get-Command $cmd -ErrorAction SilentlyContinue
    if ($encontrado) {
        $version = (& $cmd --version) 2>$null
        Ok "$cmd -> $version"
    } else {
        Mal "$cmd no esta instalado o no esta en el PATH"
    }
}

Titulo "Entorno virtual de Python"
$python = Join-Path $raiz ".venv\Scripts\python.exe"
if (Test-Path $python) {
    Ok "Existe .venv (creado en Windows)"
    & $python -m pip install -r requirements.txt --quiet 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) { Ok "Dependencias de Python instaladas" }
    else { Mal "Faltan dependencias: ejecuta .venv\Scripts\python.exe -m pip install -r requirements.txt" }
} else {
    Mal "No existe .venv. Ejecuta: python -m venv .venv"
}

Titulo "Configuracion"
if (Test-Path ".env") {
    Ok "Existe .env"
    $contenido = Get-Content ".env" -Raw
    $faltantes = @()
    foreach ($clave in @("DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD", "DB_SSL", "SECRET_KEY")) {
        if ($contenido -notmatch "(?m)^$clave\s*=\s*\S+") { $faltantes += $clave }
    }
    if ($faltantes.Count -eq 0) { Ok ".env tiene todas las variables necesarias" }
    else { Mal "Faltan variables en .env: $($faltantes -join ', ')" }
    if ($contenido -match "tu_usuario|tu_password|cambia-esta-clave") {
        Aviso ".env todavia tiene valores de ejemplo: cambialos por los reales de Neon"
    }
} else {
    Mal "No existe .env. Ejecuta: copy .env.example .env"
}

if (Test-Path "frontend\node_modules") { Ok "Las dependencias del frontend estan instaladas" }
else { Mal "Faltan las dependencias del frontend. Ejecuta: cd frontend ; npm install" }

if (Test-Path "frontend\.env") { Ok "Existe frontend\.env" }
else { Aviso "No existe frontend\.env (opcional en local: el proxy ya apunta a localhost:8000)" }

Titulo "Base de datos"
$codigo = @'
import os, sys
from dotenv import load_dotenv
load_dotenv()
try:
    import psycopg2
except ImportError:
    print("FALTA: psycopg2 no esta instalado"); sys.exit(1)
try:
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"), port=int(os.getenv("DB_PORT", "5432")),
        dbname=os.getenv("DB_NAME"), user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        sslmode="require" if os.getenv("DB_SSL", "true").lower() == "true" else "disable",
        connect_timeout=10,
    )
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM greenhouses")
    print(f"OK: conexion correcta, {cur.fetchone()[0]} invernaderos en la base de datos")
    cur.execute("SELECT count(*) FROM usuario")
    print(f"OK: {cur.fetchone()[0]} usuarios registrados")
    conn.close()
except Exception as exc:
    print(f"FALLA: {type(exc).__name__}: {exc}")
    sys.exit(1)
'@
$scriptPython = Join-Path $env:TEMP "verificar_bd.py"
Set-Content -Path $scriptPython -Value $codigo -Encoding UTF8
$salida = & $python $scriptPython 2>&1
foreach ($linea in $salida) {
    if ("$linea" -match "^OK") { Ok "$linea" } else { Mal "$linea" }
}
Remove-Item $scriptPython -ErrorAction SilentlyContinue

Titulo "API y frontend levantados"
try {
    $salud = Invoke-RestMethod "http://localhost:8000/health" -TimeoutSec 5
    Ok "La API responde en http://localhost:8000/health ($salud.status)"
} catch {
    Mal "La API no responde en el puerto 8000. Levanta la terminal 1 (scripts\iniciar_api.ps1)"
}
try {
    $proxy = Invoke-RestMethod "http://localhost:5173/api/health" -TimeoutSec 5
    Ok "El proxy del frontend funciona ($proxy.status)"
} catch {
    Mal "El frontend no responde en el puerto 5173. Levanta la terminal 2 (scripts\iniciar_frontend.ps1)"
}

Titulo "Pruebas automatizadas"
& $python -m pytest tests\ -q 2>&1 | Select-Object -Last 3 | ForEach-Object { Write-Host "  $_" }

Titulo "Resumen"
if ($fallos -eq 0) {
    Write-Host "  Todo listo. Levanta la API (terminal 1) y el frontend (terminal 2)." -ForegroundColor Green
} else {
    Write-Host "  Hay $fallos comprobacion(es) pendiente(s). Revisa lo marcado arriba." -ForegroundColor Yellow
}
Write-Host ""
