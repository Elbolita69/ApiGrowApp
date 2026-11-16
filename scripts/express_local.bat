@echo off
REM Levanta la API auxiliar (Express + MySQL en Aiven) en esta ventana.
cd /d "%~dp0..\express-api"
if not exist ".env" (
  echo [AVISO] Falta express-api\.env con MYSQL_URL. Los modulos externos no van a funcionar.
  echo         Copia express-api\.env.example a express-api\.env y pega la URL de Aiven.
  pause
  exit /b 1
)
if not exist "node_modules" (
  echo Instalando dependencias de la API auxiliar...
  call npm install
)
echo API auxiliar en http://localhost:3000
echo Presiona Ctrl+C para detenerla.
echo.
call npm start
