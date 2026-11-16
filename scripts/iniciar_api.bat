@echo off
REM Arranca la API principal (FastAPI + PostgreSQL) en Windows.
setlocal
cd /d "%~dp0.."
if not exist ".venv\Scripts\python.exe" (
  echo No existe .venv. Ejecuta primero scripts\instalar_dependencias.ps1
  exit /b 1
)
if not exist ".env" (
  echo Falta el archivo .env. Copia .env.example a .env y completa los datos.
  exit /b 1
)
".venv\Scripts\python.exe" -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
