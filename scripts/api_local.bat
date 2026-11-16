@echo off
REM Levanta la API principal (FastAPI + PostgreSQL) en esta ventana.
cd /d "%~dp0.."
echo API en http://localhost:8000  (documentacion: http://localhost:8000/docs)
echo Presiona Ctrl+C para detenerla.
echo.
".venv\Scripts\python.exe" -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
