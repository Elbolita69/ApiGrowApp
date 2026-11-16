@echo off
REM Levanta el frontend (SvelteKit) en esta ventana.
cd /d "%~dp0..\frontend"
echo Frontend en http://localhost:5173
echo Presiona Ctrl+C para detenerlo.
echo.
call npm run dev
