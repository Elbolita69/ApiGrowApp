@echo off
REM Arranca el frontend (SvelteKit) en Windows.
setlocal
cd /d "%~dp0..\frontend"
if not exist "node_modules" (
  echo Faltan las dependencias. Ejecuta primero scripts\instalar_dependencias.ps1
  exit /b 1
)
call npm run dev
