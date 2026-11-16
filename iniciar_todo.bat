@echo off
REM =====================================================================
REM  GrowApp - Inicia la API y el frontend en dos ventanas separadas.
REM  Doble clic en este archivo. Para cerrar, cerrá las dos ventanas
REM  o presiona Ctrl+C en cada una.
REM =====================================================================
setlocal
cd /d "%~dp0"

echo.
echo ============================================
echo   GrowApp - Invernadero Inteligente
echo ============================================
echo.

REM --- 1. Comprobaciones previas -------------------------------------
where python >nul 2>nul
if errorlevel 1 (
  echo [FALTA] Python no esta instalado o no esta en el PATH.
  echo         Descargalo de https://www.python.org/downloads/windows/
  echo         y marcá "Add python.exe to PATH" al instalarlo.
  pause
  exit /b 1
)

where npm >nul 2>nul
if errorlevel 1 (
  echo [FALTA] Node.js no esta instalado o no esta en el PATH.
  echo         Descargalo de https://nodejs.org/ (version LTS).
  pause
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo [FALTA] No existe el entorno virtual .venv.
  echo         Ejecuta primero:  powershell -ExecutionPolicy Bypass -File scripts\instalar_dependencias.ps1
  pause
  exit /b 1
)

if not exist ".env" (
  echo [FALTA] No existe el archivo .env con las credenciales de la base de datos.
  echo         Ejecuta:  copy .env.example .env   y completalo.
  pause
  exit /b 1
)

if not exist "frontend\node_modules" (
  echo [AVISO] Faltan las dependencias del frontend. Instalando...
  pushd frontend
  call npm install
  popd
)

REM --- 2. Mostrar las versiones --------------------------------------
echo.
echo Python:   & ".venv\Scripts\python.exe" --version
echo Node:     node --version
echo npm:      call npm --version
echo.

REM --- 3. Levantar la API en su propia ventana ------------------------
echo Levantando la API en http://localhost:8000 ...
start "GrowApp - API" cmd /k call "%~dp0scripts\api_local.bat"

REM --- 4. Esperar a que la API responda ------------------------------
echo Esperando a que la API este lista...
timeout /t 12 /nobreak >nul

REM --- 5. Levantar el frontend en su propia ventana -------------------
echo Levantando el frontend en http://localhost:5173 ...
start "GrowApp - Frontend" cmd /k call "%~dp0scripts\frontend_local.bat"

REM --- 6. Abrir el navegador -----------------------------------------
timeout /t 12 /nobreak >nul
start "" http://localhost:5173

echo.
echo ============================================
echo   Todo listo:
echo     Frontend:  http://localhost:5173
echo     API:       http://localhost:8000
echo     Documentacion de la API: http://localhost:8000/docs
echo.
echo   Usuario de prueba:  admin  /  Admin123*
echo ============================================
echo.
echo Las dos ventanas quedaron abiertas. Cerralas para detener el proyecto.
echo.
pause
