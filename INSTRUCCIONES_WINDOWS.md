# Guía paso a paso para ejecutar GrowApp en Windows

Documento de arranque para el PC con Windows 10/11. Todo lo que aparece aquí está verificado contra el proyecto: los comandos son de PowerShell y no hay ningún paso que dependa de macOS o Linux.

- **Ruta del proyecto:** `C:\Users\duvan\OneDrive\Escritorio\Nueva carpeta\ApiGrowApp-main`
- **Abrir en VS Code:** `code "C:\Users\duvan\OneDrive\Escritorio\Nueva carpeta\ApiGrowApp-main"`
- **Puertos que usa el proyecto:** `8000` (API FastAPI), `5173` (frontend SvelteKit), `3000` (API auxiliar Express, opcional)

---

## Índice

1. [Antes de empezar: qué necesitas](#1-antes-de-empezar-qué-necesitas)
2. [Abrir el proyecto en VS Code](#2-abrir-el-proyecto-en-vs-code)
3. [Instalar Python y Node.js](#3-instalar-python-y-nodejs)
4. [Instalar las dependencias del proyecto](#4-instalar-las-dependencias-del-proyecto)
5. [Configurar las variables de entorno](#5-configurar-las-variables-de-entorno)
6. [Cargar la base de datos en Neon](#6-cargar-la-base-de-datos-en-neon)
7. [Levantar la API](#7-levantar-la-api)
8. [Levantar el frontend](#8-levantar-el-frontend)
9. [Entrar al sistema](#9-entrar-al-sistema)
10. [API auxiliar Express (opcional)](#10-api-auxiliar-express-opcional)
11. [Verificación final](#11-verificación-final)
12. [Problemas frecuentes](#12-problemas-frecuentes)
13. [Cómo volver a levantar el proyecto otro día](#13-cómo-volver-a-levantar-el-proyecto-otro-día)
14. [Dónde está cada cosa](#14-dónde-está-cada-cosa)
15. [Publicarlo en Render](#15-publicarlo-en-render)

---

## 1. Antes de empezar: qué necesitas

| Herramienta | Versión | Para qué | Cómo la verificas |
|---|---|---|---|
| Python | 3.11 o superior | La API (FastAPI) | `python --version` |
| Node.js | 20 o superior | El frontend (SvelteKit) | `node --version` y `npm --version` |
| VS Code | Cualquiera | Editar el código | `code --version` |
| Cuenta en Neon | — | La base de datos PostgreSQL | <https://neon.tech> (gratis) |
| Cuenta en Railway | — | Solo la API auxiliar | <https://railway.app> (opcional) |

**Si `python --version` no funciona**, es casi siempre porque al instalar Python no marcaste la casilla *"Add python.exe to PATH"*. Reinstálalo y márcala, o usa el **Launcher de Python** de python.org para instalar Python 3.12.

---

## 2. Abrir el proyecto en VS Code

### Opción A: desde la terminal (la más rápida)

Abre **PowerShell** (clic derecho en el menú Inicio → *Terminal* → *PowerShell*) y ejecuta:

```powershell
code "C:\Users\duvan\OneDrive\Escritorio\Nueva carpeta\ApiGrowApp-main"
```

> Si `code` no está reconocido, es que VS Code no está en el PATH. Ábrelo manualmente una vez y, desde VS Code, ejecuta `Ctrl+Shift+P` → **Preferences: Configure Shell PATH** → marca *Include VS Code's installation in the shell PATH*.

### Opción B: desde la interfaz de VS Code

1. Abre VS Code.
2. `Ctrl+K Ctrl+O` (o *File → Open Folder…*).
3. Pega la ruta: `C:\Users\duvan\OneDrive\Escritorio\Nueva carpeta\ApiGrowApp-main`
4. *Select Folder*.

### Extensiones recomendadas

VS Code te va a pedir instalar las extensiones para Svelte. Acepta la sugerencia de **Svelte for VS Code** (`svelte.svelte-vscode`).

### Terminales de VS Code

Vas a necesitar **dos terminales** (una para la API y otra para el frontend). Abrir una terminal en la raíz del proyecto: `Ctrl+Ñ` (o *Terminal → New Terminal*). Para crear una segunda: clic en el icono `+` en el panel de terminals.

> **Atención con OneDrive:** OneDrive sincroniza los archivos continuamente. Si ves que el explorador de VS Code marca archivos como "sincronizando", el proyecto sigue funcionando; solo ten en cuenta que las primeras instalaciones pueden ir algo lentas.

---

## 3. Instalar Python y Node.js

Abre **PowerShell** y comprueba:

```powershell
python --version
node --version
npm --version
```

- Si Python no está instalado: <https://www.python.org/downloads/windows/> → *Download Windows installer (64-bit)* → al instalar, **marca "Add python.exe to PATH"**.
- Si Node.js no está instalado: <https://nodejs.org/> → descarga la versión **LTS** (20 o superior) → instalador `.msi` → siguiente, siguiente, siguiente.

Vuelve a abrir PowerShell después de instalar para que los comandos nuevos se reconozcan.

---

## 4. Instalar las dependencias del proyecto

### 4.1 Todo con un solo script (lo más rápido)

Desde la **raíz del proyecto** en PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\instalar_dependencias.ps1
```

Ese script hace las tres cosas de los siguientes apartados. Si prefieres hacerlo a mano, sigue leyendo.

### 4.2 Dependencias de Python (API)

```powershell
cd "C:\Users\duvan\OneDrive\Escritorio\Nueva carpeta\ApiGrowApp-main"

python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Notas importantes:**

- El comando para activar es `.\.venv\Scripts\Activate.ps1` (Windows). `source .venv/bin/activate` es de macOS y **no funciona aquí**.
- Si PowerShell dice *"La ejecución de scripts está deshabilitada en este sistema"*, ejecuta una sola vez:

  ```powershell
  Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
  ```

  y vuelve a intentarlo.
- Si prefieres no activar el entorno, usa siempre el ejecutable directo:

  ```powershell
  .\.venv\Scripts\python.exe -m pip install -r requirements.txt
  ```

- La línea `(venv) PS C:\...>` en el prompt confirma que el entorno está activo.

### 4.3 Dependencias del frontend

```powershell
cd frontend
npm install
cd ..
```

> **Importante:** el proyecto **no** incluye `node_modules` (venía de un Mac con binarios que no funcionan en Windows). El `npm install` de arriba los regenera para tu equipo. Tarda un par de minutos la primera vez.

### 4.4 Dependencias de la API auxiliar (solo si la vas a usar)

```powershell
cd express-api
npm install
cd ..
```

---

## 5. Configurar las variables de entorno

### 5.1 La API (archivo `.env` en la raíz)

```powershell
copy .env.example .env
```

Abre `.env` en VS Code y completa estos valores con los datos de **Neon** (en Neon: *Dashboard → Connection Details*):

```env
DB_HOST=ep-xxxxxxxx-xxxxx.us-east-2.aws.neon.tech
DB_PORT=5432
DB_NAME=growapp
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_SSL=true
SECRET_KEY=una-clave-larga-y-aleatoria
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

**Sobre `SECRET_KEY`**: es la clave con la que se firman los tokens de sesión. Genera una larga y aleatoria con este comando de PowerShell:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Copia el resultado y pégalo en `SECRET_KEY`.

### 5.2 El frontend (archivo `.env` dentro de `frontend/`)

```powershell
cd frontend
copy .env.example .env
cd ..
```

El archivo que se crea ya trae los valores correctos para desarrollo:

```env
VITE_API_TARGET=http://localhost:8000
VITE_EXPRESS_TARGET=http://localhost:3000
```

No hay que cambiar nada. Las variables `VITE_API_URL` y `VITE_EXPRESS_URL` solo se usan al publicar el sitio en internet.

---

## 6. Cargar la base de datos en Neon

El archivo `schema.sql` crea las 16 tablas, sus campos de auditoría, los índices, los triggers y los datos de prueba. **Es idempotente**: puedes ejecutarlo varias veces.

### Opción A: desde el sitio de Neon (la más fácil)

1. Entra en <https://console.neon.tech> y abre tu proyecto.
2. Menú **SQL Editor** → **New query**.
3. Abre `schema.sql` en VS Code, selecciona todo (`Ctrl+A`) y cópialo (`Ctrl+C`).
4. Pégalo en el editor de Neon y pulsa **Run**.

Cuando termine verás el mensaje de éxito y la lista de tablas en el panel lateral.

### Opción B: desde la terminal con `psql`

Si tienes `psql` en el PATH:

```powershell
psql "postgresql://TU_USUARIO:TU_PASSWORD@ep-xxxxxxxx.us-east-2.aws.neon.tech/growapp?sslmode=require" -f schema.sql
```

### Opción C: con una base de datos PostgreSQL local

Si prefieres trabajar en local (más rápido y sin depender de internet):

1. Instala PostgreSQL 15 o superior: <https://www.postgresql.org/download/windows/>
2. During la instalación, anota la contraseña del usuario `postgres`.
3. Crea la base de datos:

   ```powershell
   createdb -U postgres growapp
   ```

4. Carga el esquema:

   ```powershell
   psql -U postgres -d growapp -f schema.sql
   ```

5. En tu `.env` de la raíz cambia:

   ```env
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=growapp
   DB_USER=postgres
   DB_PASSWORD=la-que-poniste-al-instalar
   DB_SSL=false
   ```

### Cómo comprobar que se cargó

El proyecto incluye un script de diagnóstico que revisa **todo** (herramientas, `.env`, conexión a la base de datos, API, frontend y pruebas). Úsalo en cualquier momento:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\verificar.ps1
```

Te dirá línea por línea qué está bien y qué falta. En la parte de la base de datos debe decir `OK: conexion correcta, 20 invernaderos en la base de datos`.

---

## 7. Levantar la API

En la **terminal 1** (con el entorno virtual activado):

```powershell
cd "C:\Users\duvan\OneDrive\Escritorio\Nueva carpeta\ApiGrowApp-main"
.\.venv\Scripts\Activate.ps1
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

O con el script incluido (no necesita activar el entorno):

```powershell
powershell -ExecutionPolicy Bypass -File scripts\iniciar_api.ps1
```

### Debe verse así

```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Comprueba que responde

Abre en el navegador: <http://localhost:8000/health>

Debe mostrar:

```json
{"status":"healthy"}
```

Y la documentación interactiva: <http://localhost:8000/docs>

> **Deja esa terminal abierta.** La API se queda corriendo; `Ctrl+C` la detiene.

---

## 8. Levantar el frontend

En la **terminal 2**:

```powershell
cd "C:\Users\duvan\OneDrive\Escritorio\Nueva carpeta\ApiGrowApp-main\frontend"
npm run dev
```

### Debe verse así

```
  VITE v8.3.5  ready in 3 s

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

Abre <http://localhost:5173> en el navegador. Deberías ver la pantalla de login con el logo verde de GrowApp.

> **La terminal 2 también queda ocupada.** `Ctrl+C` detiene el frontend.

---

## 9. Entrar al sistema

En <http://localhost:5173> usa uno de estos usuarios de prueba (vienen creados en `schema.sql`):

| Rol | Usuario | Contraseña | Qué puede hacer |
|---|---|---|---|
| administrador | `admin` | `Admin123*` | Todo: usuarios, roles, todos los módulos |
| supervisor | `supervisor1` | `Supervisor123*` | Casi todo, sin eliminar usuarios |
| agronomo | `agronomo1` | `Agronomo123*` | Cultivos, lotes, parámetros, alertas |
| regador | `regador1` | `Regador123*` | Riego, zonas, actuadores, sensores |
| tecnico | `tecnico1` | `Tecnico123*` | Sensores, lecturas, actuadores |
| lector | `lector1` | `Lector123*` | Solo consultar (8 módulos) |
| auxiliar_riego | `auxiliar_riego1` | `AuxiliarRiego123*` | Zonas e historial de riego |
| planificador | `planificador1` | `Planificador123*` | Planificación de siembras |
| calidad | `calidad1` | `Calidad123*` | Revisión de alertas y lecturas |
| mantenimiento | `mantenimiento1` | `Mantenimiento123*` | Mantenimiento de equipos |

**Prueba recomendada:** entra con `admin` y con `lector1` en sesiones distintas (o en una ventana incógnita) para ver cómo el menú cambia según el rol.

> Cambia estas contraseñas antes de entregar el proyecto.

### Módulos disponibles en el menú

Invernaderos · Sensores · Lecturas de sensores · Cultivos · Lotes de cultivo · Alertas · Zonas de riego · Historial de riego · Actuadores · Control de actuadores · Parámetros del invernadero · Usuarios · Estudiantes · Sensores externos · Lecturas externas · Alertas externas · **Asistente**

---

## 10. API auxiliar Express (opcional)

Solo hace falta si vas a usar los tres módulos de datos meteorológicos externos (sensores externos, lecturas externas, alertas externas), que viven en MySQL (Railway).

1. Crea una base de datos MySQL en <https://railway.app> y carga `express-api/schema.sql` en su editor SQL.
2. Crea `express-api\.env`:

   ```powershell
   cd express-api
   copy .env.example .env
   cd ..
   ```

3. Completa `MYSQL_URL` con los datos de Railway:

   ```env
   MYSQL_URL=mysql://usuario:contrasena@host:3306/nombre_base
   PORT=3000
   ```

4. En una **terminal 3**:

   ```powershell
   cd "C:\Users\duvan\OneDrive\Escritorio\Nueva carpeta\ApiGrowApp-main\express-api"
   npm start
   ```

5. Comprueba: <http://localhost:3000/health> → `{"status":"ok", ...}`

> Si no la levantas, los tres módulos externos dan error y el resto funciona con normalidad.

---

## 11. Verificación final

Con la API y el frontend levantados, en una tercera terminal:

```powershell
cd "C:\Users\duvan\OneDrive\Escritorio\Nueva carpeta\ApiGrowApp-main"

# 1. La API responde
curl.exe http://localhost:8000/health

# 2. El login funciona (devuelve un token)
curl.exe -X POST -d "username=admin&password=Admin123*" http://localhost:8000/auth/login

# 3. El proxy del frontend llega a la API
curl.exe http://localhost:5173/api/health

# 4. Las pruebas automatizadas pasan
.\.venv\Scripts\python.exe -m pytest tests\ -q
```

Los cuatro deben responder bien. El cuarto debe terminar con `113 passed`.

Para parar todo: `Ctrl+C` en cada terminal.

---

## 12. Problemas frecuentes

### `'python' no se reconoce como comando`
Abre **Configuración → Aplicaciones → Alias de ejecución de Python** en Windows y activa los dos interruptores. O reinstala Python marcando *"Add python.exe to PATH"*.

### `.\.venv\Scripts\Activate.ps1: no se puede cargar el archivo... la ejecución de scripts está deshabilitada`
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```
Cierra PowerShell, vuelve a abrirlo y repite el `Activate.ps1`.

### `npm : el término 'npm' no se reconoce`
Node.js no está instalado o no está en el PATH. Reinstálalo y **abre una terminal nueva**.

### `svelte-kit sync` falla o `Cannot find module '@sveltejs/kit'`
Faltan las dependencias del frontend:
```powershell
cd frontend
npm install
```

### `npm install` se queda colgado o da error de permisos o `ENOENT`
Borra `node_modules` y vuelve a instalar:
```powershell
cd frontend
Remove-Item -Recurse -Force node_modules
npm install
```

### La API devuelve `503 - No se pudo conectar con la base de datos`
Los datos de `.env` no coinciden con los de Neon. Revisa `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` y que `DB_SSL=true` para Neon.

Comprueba la conexión:
```powershell
.\.venv\Scripts\python.exe -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('DB_HOST'), os.getenv('DB_NAME'))"
```

### El login dice `Credenciales incorrectas`
La base de datos no tiene los usuarios sembrados. Carga `schema.sql` en Neon (paso 6).

### El frontend carga pero los módulos salen vacíos o en error
Comprueba que la API esté arriba (<http://localhost:8000/health>) y que el proxy funcione (<http://localhost:5173/api/health>).

### El navegador guarda la sesión old y no deja entrar
Borrar el `localStorage` del sitio: `Ctrl+Shift+Del` → Borrar datos → o abre una ventana incógnita.

### OneDrive bloquea algunos archivos
OneDrive a veces deja archivos en solo lectura o los marca como "sincronizando". Si un comando falla con un error de permisos, cierra OneDrive temporalmente desde el icono de la bandeja del sistema.

### Cambié el código y no se refleja
- Frontend: el servidor de Vite recarga solo. Si no, reinicia `npm run dev`.
- Backend: uvicorn corre con `--reload`, también recarga solo. Si no, revisa que la terminal 1 no esté congelada.

---

## 13. Cómo volver a levantar el proyecto otro día

No hace falta repetir nada de la instalación. Solo dos terminales:

**Terminal 1 — la API:**
```powershell
cd "C:\Users\duvan\OneDrive\Escritorio\Nueva carpeta\ApiGrowApp-main"
.\.venv\Scripts\Activate.ps1
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 — el frontend:**
```powershell
cd "C:\Users\duvan\OneDrive\Escritorio\Nueva carpeta\ApiGrowApp-main\frontend"
npm run dev
```

Y abrir <http://localhost:5173>.

Atajos: `scripts\iniciar_api.bat` y `scripts\iniciar_frontend.bat` hacen lo mismo con doble clic o con una línea de comando.

Si algo no cuadra, ejecuta el diagnóstico:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\verificar.ps1
```

---

## 14. Dónde está cada cosa

```
ApiGrowApp-main/
├── main.py                  Punto de entrada de la API
├── requirements.txt         Dependencias de Python
├── schema.sql               Esquema de PostgreSQL + datos de prueba (16 tablas)
├── .env                     TUS credenciales de Neon (no se sube a internet)
├── .env.example             Plantilla del .env
│
├── app/                     API FastAPI
│   ├── api/                 Routers (uno por módulo)
│   ├── core/                database.py (pool psycopg2), auth.py (JWT), asistente.py
│   ├── models/              Modelos Pydantic v2
│   └── repositories/        SQL puro con psycopg2
│
├── frontend/                Frontend SvelteKit
│   ├── svelte.config.js
│   ├── vite.config.js       Proxy /api -> localhost:8000
│   └── src/
│       ├── lib/components/  16 componentes reutilizables
│       ├── lib/services/    Única capa que hace fetch (19 archivos)
│       └── routes/          +layout.svelte y +page.svelte
│
├── express-api/             API auxiliar (Express + MySQL), opcional
├── scripts/                 Scripts .ps1 y .bat para Windows
├── tests/                   113 pruebas automatizadas
└── odd/tasks/port-windows.md   Especificación y bitácora del taller
```

### Tablas de la base de datos (16)

| Tabla | Qué guarda |
|---|---|
| `rol` | Los 10 roles del sistema |
| `modulo` | Los 16 módulos de la aplicación |
| `moduloxrol` | Qué puede hacer cada rol en cada módulo |
| `usuario` | Los usuarios y su rol |
| `greenhouses` | Invernaderos |
| `sensors` | Sensores |
| `sensor_readings` | Lecturas de sensores |
| `crops` | Catálogo de cultivos |
| `crop_batches` | Lotes de cultivo |
| `alerts` | Alertas |
| `irrigation_zones` | Zonas de riego |
| `irrigation_logs` | Historial de riego |
| `actuators` | Actuadores |
| `actuator_controls` | Órdenes de control |
| `greenhouse_settings` | Parámetros agronómicos |
| `estudiantes` | Estudiantes del programa |

**Todas** tienen `creado`, `actualizado` y `estado`. `estado` es el borrado lógico: cuando "eliminas" algo, se marca como `FALSE` y el registro **nunca** se borra de la base de datos.

---

## Si algo falla y no encuentras la causa

1. Copia el mensaje de error exacto.
2. Anota en qué terminal aparece (API o frontend).
3. Revisa la sección [Problemas frecuentes](#12-problemas-frecuentes).

Los logs quedan en la terminal donde se levantó cada servicio.

---

## 15. Publicarlo en Render

La base de datos ya está en **Neon** (completa con tus credenciales). En Render solo se publica el código, en dos servicios.

### 15.1 La API (Web Service)

En <https://dashboard.render.com> → **New → Web Service** → conecta el repositorio.

| Campo | Valor |
|---|---|
| Root Directory | *(vacío)* |
| Runtime | Python |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn main:app --host 0.0.0.0 --port $PORT` |

> **Ojo:** en el Start Command **no** pongas `--reload`. Eso es solo para tu PC.

En *Environment* agrega estas variables con los datos de Neon:

```
DB_HOST=ep-xxxxxxxx-pooler.c-9.us-east-2.aws.neon.tech
DB_PORT=5432
DB_NAME=neondb
DB_USER=neondb_owner
DB_PASSWORD=la_de_neon
DB_SSL=true
SECRET_KEY=una_clave_larga_y_aleatoria
CORS_ORIGINS=https://tu-frontend.onrender.com
DB_POOL_MIN=10
DB_POOL_MAX=15
```

- Usa el host **con `-pooler`**: es el que aguanta varias conexiones simultáneas.
- `SECRET_KEY` la generas con `python -c "import secrets; print(secrets.token_urlsafe(48))"`.
- `CORS_ORIGINS` lo completas en el paso 15.2.

Comprueba que quedó viva: <https://tu-api.onrender.com/health> → `{"status":"healthy"}`

### 15.2 El frontend (Static Site)

En <https://dashboard.render.com> → **New → Static Site** → mismo repositorio.

| Campo | Valor |
|---|---|
| Root Directory | `frontend` |
| Build Command | `npm install && npm run build` |
| Publish Path | `build` |

En *Environment*:

```
VITE_API_URL=https://tu-api.onrender.com
```

En *Settings → Redirects/Headers* agrega la regla:

| Source | Destination | Status |
|---|---|---|
| `/*` | `/index.html` | 200 (Rewrite) |

> Las variables `VITE_*` se leen **al compilar**. Si las cambias, hay que recompilar el sitio.

### 15.3 El orden completo

1. Despliega la **API** → anota `https://tu-api.onrender.com`
2. Despliega el **frontend** con `VITE_API_URL` = esa URL → anota `https://tu-frontend.onrender.com`
3. Vuelve a la **API** y pon `CORS_ORIGINS=https://tu-frontend.onrender.com`
4. Abre el frontend y entra con `admin` / `Admin123*`

### 15.4 Comprobar desde tu PC

```powershell
curl.exe https://tu-api.onrender.com/health
curl.exe -X POST -d "username=admin&password=Admin123*" https://tu-api.onrender.com/auth/login
curl.exe https://tu-frontend.onrender.com
```

> El plan gratuito de Render se duerme tras 15 minutos sin uso: la primera petición después de dormir tarda más (arranque en frío). No es un error.
