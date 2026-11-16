# GrowApp - Invernadero Inteligente

API REST y panel web para la gestion de invernaderos inteligentes (cultivos, sensores, riego, actuadores y alertas) con **FastAPI + PostgreSQL (Neon)** y **SvelteKit**.

> Este proyecto fue migrado desde macOS y esta verificado para ejecutarse en **Windows 10/11**. No hay scripts de bash ni rutas tipo `/Users/...`: todos los comandos son multiplataforma y se ejecutan con `python -m ...` y `npm run ...`.

## Tabla de Contenidos

1. [Autores](#autores)
2. [Requisitos previos](#requisitos-previos)
3. [Instalacion paso a paso en Windows](#instalacion-paso-a-paso-en-windows)
4. [Estructura del proyecto](#estructura-del-proyecto)
5. [Arquitectura](#arquitectura)
6. [Base de datos principal (PostgreSQL - Neon)](#base-de-datos-principal-postgresql---neon)
7. [Base de datos auxiliar (MySQL - Aiven)](#base-de-datos-auxiliar-mysql---aiven)
8. [Autenticacion, JWT y permisos por rol](#autenticacion-jwt-y-permisos-por-rol)
9. [Endpoints de la API](#endpoints-de-la-api)
10. [Asistente de consultas en lenguaje natural](#asistente-de-consultas-en-lenguaje-natural)
11. [Frontend SvelteKit](#frontend-sveltekit)
12. [Pruebas](#pruebas)
13. [Despliegue](#despliegue)
14. [Reglas de negocio implementadas](#reglas-de-negocio-implementadas)

---

## Autores

- Esteban Gomez Jimenez
- Victor Daniel Amaranto Garizabalo
- Jose Muñoz Perez

---

## Requisitos previos

| Herramienta | Version | Nota |
|---|---|---|
| Python | 3.11 o superior | `python --version`. En Windows marca "Add python.exe to PATH" al instalar. |
| Node.js | 20 o superior | `node --version`. |
| PostgreSQL | 15 o superior | Solo si usas una base local; en la nube usas Neon. |
| MySQL / MariaDB | 8 o superior | Solo para la API auxiliar. |

---

## Instalacion paso a paso en Windows

### 1. Obtener el proyecto

Abre **PowerShell** en la carpeta del proyecto:

```powershell
cd "C:\Users\duvan\OneDrive\Escritorio\Nueva carpeta\ApiGrowApp-main"
```

### 2. Crear el entorno virtual de Python

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Si PowerShell bloquea la activacion por politica de ejecucion:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Alternativa sin activar el entorno, usando el ejecutable directamente:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

> **No uses `python3`**: en Windows el comando es `python`. Y no uses `source .venv/bin/activate` (eso es de macOS/Linux); en Windows es `.\.venv\Scripts\Activate.ps1`.

### 3. Configurar las variables de entorno

```powershell
copy .env.example .env
```

Edita `.env` con tus credenciales de Neon:

```
DB_HOST=ep-xxxxxxxx.us-east-2.aws.neon.tech
DB_PORT=5432
DB_NAME=growapp
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_SSL=true
SECRET_KEY=una-clave-larga-y-aleatoria
CORS_ORIGINS=http://localhost:5173
```

Y en `frontend/`:

```powershell
cd frontend
copy .env.example .env
cd ..
```

### 4. Instalar las dependencias del frontend

```powershell
cd frontend
npm install
cd ..
```

> El proyecto no incluye `node_modules`: se instala en tu equipo para que los binarios nativos correspondan a tu sistema (Windows), no a macOS.

### 5. Cargar la base de datos

Ejecuta `schema.sql` completo en tu base de datos (Neon o local). El archivo es idempotente: empieza con `DROP TABLE IF EXISTS ... CASCADE` y recrea todo con datos de prueba.

En Neon, abre el **SQL Editor**, pega el contenido de `schema.sql` y ejecuta.

En una base local con `psql` en el PATH:

```powershell
psql -h localhost -U postgres -d growapp -f schema.sql
```

### 6. Levantar la API

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

O con el script incluido:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\iniciar_api.ps1
```

Verifica en el navegador: <http://localhost:8000/docs> (documentacion interactiva) y <http://localhost:8000/health>.

### 7. Levantar el frontend

En otra terminal:

```powershell
cd frontend
npm run dev
```

Abre <http://localhost:5173>.

### 8. (Opcional) Levantar la API auxiliar

```powershell
cd express-api
copy .env.example .env
npm install
npm start
```

### Scripts de ayuda

En `scripts/` hay tareas para Windows que evitan repetir comandos a mano. La guía completa, paso a paso, está en **[INSTRUCCIONES_WINDOWS.md](INSTRUCCIONES_WINDOWS.md)**:

| Script | Que hace |
|---|---|
| `scripts\instalar_dependencias.ps1` | Crea `.venv`, instala Python, `npm install` del frontend y de `express-api`. |
| `scripts\verificar.ps1` | Diagnostico completo: comprueba herramientas, `.env`, base de datos, API, frontend y pruebas. |
| `scripts\iniciar_api.ps1` / `.bat` | Levanta la API en el puerto 8000 con recarga. |
| `scripts\iniciar_frontend.ps1` / `.bat` | Levanta el frontend en el puerto 5173. |
| `scripts\iniciar_api_express.ps1` | Levanta la API auxiliar en el puerto 3000. |

---

## Estructura del proyecto

```
ApiGrowApp-main/
├── app/                          # API principal (FastAPI)
│   ├── api/                      # Routers (uno por modulo)
│   │   ├── rutas_auth.py
│   │   ├── rutas_greenhouse.py
│   │   ├── rutas_sensor.py
│   │   ├── rutas_sensor_reading.py
│   │   ├── rutas_crop.py
│   │   ├── rutas_crop_batch.py
│   │   ├── alertas / riego / actuadores ...
│   │   ├── rutas_user.py
│   │   ├── rutas_rol.py
│   │   ├── rutas_estudiante.py
│   │   └── rutas_asistente.py
│   ├── core/
│   │   ├── auth.py               # JWT + permisos por rol (moduloxrol)
│   │   ├── database.py           # Pool psycopg2 (ThreadedConnectionPool)
│   │   └── asistente.py          # get_schema() / run_sql_query() / lenguaje natural
│   ├── models/                   # Modelos Pydantic v2
│   └── repositories/             # SQL puro con psycopg2 (sin ORM)
├── express-api/                  # API auxiliar (Express + MySQL)
├── frontend/                     # Frontend SvelteKit
│   ├── svelte.config.js
│   ├── vite.config.js            # Proxy /api -> http://localhost:8000
│   └── src/
│       ├── lib/
│       │   ├── components/       # 16 componentes reutilizables
│       │   ├── services/         # UNICA capa que hace fetch
│       │   ├── config/modulos.js
│       │   └── stores/
│       └── routes/               # +layout.svelte / +page.svelte
├── scripts/                      # .ps1 y .bat para Windows
├── tests/                        # Pruebas con base de datos simulada
├── main.py                       # Punto de entrada de FastAPI
├── requirements.txt
├── schema.sql                    # Esquema PostgreSQL + semillas
└── odd/tasks/port-windows.md     # Especificacion y tareas del taller
```

---

## Arquitectura

### API principal (FastAPI + PostgreSQL)

**Tecnologias:** FastAPI, Python 3.11+, psycopg2 (SQL puro, sin ORM), Pydantic v2, python-jose (JWT), bcrypt, Uvicorn.

Reglas de la estructura:

- `app/api/` contiene solo los routers (HTTP).
- `app/core/` contiene la infraestructura: pool de base de datos, autenticacion y el asistente.
- `app/models/` contiene los schemas de Pydantic: los de escritura **no aceptan `id`** porque el identificador lo asigna la base de datos.
- `app/repositories/` contiene el SQL. Cada metodo es una consulta parametrizada (`%s`), nunca concatenacion de cadenas.

Como `psycopg2` es sincrono, los handlers se declaran con `def` (no `async def`): FastAPI los ejecuta en su threadpool y no bloquea el event loop.

### API auxiliar (Express + MySQL)

Express.js con `mysql2` para los datos meteorologicos externos (sensores, lecturas y alertas externas). Es independiente de la API principal y opcional.

### Frontend (SvelteKit)

Svelte 5 en modo runes, `adapter-static` con `fallback: 'index.html'` (SPA), Bootstrap 5 por CDN, Bootstrap Icons y DataTables para todas las tablas.

---

## Base de datos principal (PostgreSQL - Neon)

16 tablas. Todas incluyen los tres campos de auditoria:

| Campo | Tipo | Proposito |
|---|---|---|
| `creado` | `TIMESTAMP` | Fecha y hora de creacion. |
| `actualizado` | `TIMESTAMP` | Fecha y hora de la ultima modificacion (un trigger lo refresca en cada `UPDATE`). |
| `estado` | `BOOLEAN` | Borrado **logico**: `TRUE` activo, `FALSE` eliminado. |

**El borrado fisico esta prohibido**: la API nunca ejecuta `DELETE`; el "eliminar" hace `UPDATE ... SET estado = FALSE`.

### Tablas de negocio (12)

| Tabla | Descripcion |
|---|---|
| `greenhouses` | Invernaderos (areas de cultivo) |
| `sensors` | Sensores de monitoreo |
| `sensor_readings` | Lecturas de sensores |
| `crops` | Catalogo de cultivos |
| `crop_batches` | Lotes de cultivo |
| `alerts` | Alertas del sistema |
| `irrigation_zones` | Zonas de riego |
| `irrigation_logs` | Historial de riego |
| `actuators` | Actuadores (ventanas, ventiladores, bombas, luces) |
| `actuator_controls` | Ordenes de control de actuadores |
| `greenhouse_settings` | Parametros agronomicos por invernadero |
| `estudiantes` | Estudiantes del programa (modulo CRUD del taller) |

### Tablas de control de acceso (4)

| Tabla | Descripcion |
|---|---|
| `rol` | Roles del sistema |
| `modulo` | Modulos de la aplicacion |
| `moduloxrol` | Permisos (ver/crear/editar/eliminar) por rol y modulo |
| `usuario` | Usuarios con su rol |

### Datos iniciales

- 20 registros en cada tabla de negocio.
- 10 estudiantes, 10 roles, 16 modulos y la matriz completa de `moduloxrol`.
- Los usuarios de prueba son:

| Rol | Usuario | Contrasena |
|---|---|---|
| administrador | `admin` | `Admin123*` |
| supervisor | `supervisor1`, `supervisor2` | `Supervisor123*` |
| agronomo | `agronomo1` ... `agronomo4` | `Agronomo123*` |
| regador | `regador1` ... `regador4` | `Regador123*` |
| tecnico | `tecnico1` ... `tecnico3` | `Tecnico123*` |
| lector | `lector1` ... `lector3` | `Lector123*` |
| auxiliar_riego | `auxiliar_riego1` | `AuxiliarRiego123*` |
| planificador | `planificador1` | `Planificador123*` |
| calidad | `calidad1` | `Calidad123*` |
| mantenimiento | `mantenimiento1` | `Mantenimiento123*` |

> Cambia estas contrasenas antes de entregar el proyecto.

---

## Base de datos auxiliar (MySQL - Aiven)

3 tablas: `sensores_externos`, `lecturas_externas`, `alertas_externas`, con los mismos campos de auditoria y borrado logico. Se cargan con `express-api/schema.sql`.

La base vive en el plan gratuito de MySQL de [Aiven](https://aiven.io). Su Service URI trae `?ssl-mode=REQUIRED`; `express-api/src/config/opciones.js` lo traduce a TLS para `mysql2`. Para cargar el esquema sin instalar MySQL: `cd express-api && npm run db:init` (no duplica datos si ya existen).

---

## Autenticacion, JWT y permisos por rol

### JWT

- Algoritmo `HS256`, expiracion de 24 horas, clave en `SECRET_KEY`.
- El token viaja en `Authorization: Bearer <token>` y se guarda en `localStorage`.
- Claims: `sub` (id del usuario), `username`, `rol` (nombre del rol) y `exp`.

### Permisos por rol

Cada endpoint declara el permiso que exige:

```python
@router.get("/", dependencies=[Depends(require_permission("crops", "ver"))])
```

`require_permission` consulta `moduloxrol` uneindo `rol` y `modulo` **por nombre**, y exige que la columna `puede_ver` / `puede_crear` / `puede_editar` / `puede_eliminar` sea `TRUE` y que las tres tablas esten activas.

Consecuencias:

- El menu lateral del frontend se arma con `GET /auth/modulos`, asi que **cada rol ve solo los modulos permitidos**.
- Un rol que intente saltarse el menu recibe igual `403` desde la API.
- **Reflejo de procesos**: los modulos de negocio son visibles para varios roles, de modo que lo que registra un rol lo ven los demas (por ejemplo, el agronomo registra un cultivo y el regador lo consulta).

---

## Endpoints de la API

Documentacion completa e interactiva en <http://localhost:8000/docs>.

### Auth

| Metodo | Ruta | Descripcion |
|---|---|---|
| POST | `/auth/login` | Iniciar sesion (devuelve el token) |
| POST | `/auth/register` | Registrar usuario (siempre con rol `lector`) |
| GET | `/auth/me` | Usuario autenticado |
| GET | `/auth/modulos` | Modulos y permisos del rol |

### CRUD de negocio

Todos siguen el mismo patron y filtran por `estado = TRUE`:

| Metodo | Ruta | Modulo |
|---|---|---|
| GET/POST | `/greenhouses` | Invernaderos |
| GET/PUT/DELETE | `/greenhouses/{id}` | |
| GET/POST | `/sensors` | Sensores |
| GET/PUT/DELETE | `/sensors/{id}` | |
| GET/POST | `/sensor-readings` | Lecturas |
| GET/POST | `/crops` | Cultivos |
| GET/PUT/DELETE | `/crops/{id}` | |
| GET/POST | `/crop-batches` | Lotes de cultivo |
| GET/PUT/DELETE | `/crop-batches/{id}` | |
| GET/POST | `/alerts` | Alertas |
| PATCH | `/alerts/{id}/resolver` | Resolver alerta |
| GET/POST | `/irrigation-zones` | Zonas de riego |
| GET/PUT/DELETE | `/irrigation-zones/{id}` | |
| GET/POST | `/irrigation-logs` | Historial de riego |
| GET/POST | `/actuators` | Actuadores |
| GET/PUT/DELETE | `/actuators/{id}` | |
| GET/POST | `/actuator-controls` | Control de actuadores |
| GET/POST | `/greenhouse-settings` | Parametros por invernadero |
| GET/POST | `/users` | Usuarios (CRUD completo solo para administrador) |
| GET | `/roles` | Roles activos (desplegables) |
| GET/POST | `/estudiantes` | Estudiantes del programa |

### API auxiliar (Express)

`/sensores-externos`, `/lecturas-externas`, `/alertas-externas` en `http://localhost:3000`.

---

## Asistente de consultas en lenguaje natural

`app/core/asistente.py` implementa el asistente con dos funciones internas:

- `get_schema()`: lee `information_schema.columns` para conocer la estructura de la base de datos.
- `run_sql_query(sql, params)`: ejecuta **solo** consultas `SELECT`, con validacion previa que rechaza cualquier sentencia con `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `CREATE`, `TRUNCATE`, `GRANT`, `COPY` o `;` seguido de otra sentencia, y bloquea el acceso a `pg_catalog` y `pg_*`.

El endpoint es `POST /asistente/preguntar` con `{"pregunta": "..."}` y devuelve `{"respuesta": "..."}`.

**El asistente nunca muestra SQL.** La respuesta se arma a partir del resultado de la consulta con plantillas en espanol: el usuario lee "Hay 20 invernaderos registrados: Invernadero Tomate Chonto Cajica, ..." y nunca ve una sentencia `SELECT`.

El frontend lo consume en la ruta `/asistente`.

---

## Frontend SvelteKit

### Estructura

- `src/lib/components/` - 16 componentes reutilizables en subcarpetas: `AlertBox`, `Badge`, `Card`, `ConfirmDialog`, `CrudPage`, `DataTable`, `Footer`, `FormField`, `Header`, `LoadingSpinner`, `Modal`, `Navbar`, `PageHeader`, `Sidebar`, `StatCard`, `Toast`.
- `src/lib/services/` - **la unica capa que hace `fetch`**: un nucleo (`api.js`) mas un archivo por dominio (`auth.js`, `crops.js`, `sensors.js`, ...). Las rutas y los componentes nunca llaman `fetch` directamente.
- `src/routes/` - `+layout.svelte` y `+page.svelte` unicamente. El grupo `(app)/` aporta el esqueleto con Navbar, Sidebar y Footer.

### Proxy

`vite.config.js` redirige las llamadas al backend sin CORS y sin URLs absolutas en el codigo:

```js
server: {
  proxy: {
    '/api': {
      target: process.env.VITE_API_TARGET || 'http://localhost:8000',
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/api/, '')
    },
    '/api-express': {
      target: process.env.VITE_EXPRESS_TARGET || 'http://localhost:3000',
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/api-express/, '')
    }
  }
}
```

### Formularios

`bind:value` para capturar datos, `preventDefault()` en cada envio y `onMount()` para la carga inicial.

### Los IDs no se ven

En ningun modulo se muestra un identificador de base de datos, y no existe ningun campo para escribirlo. Las llaves foraneas se eligen **por nombre** en un desplegable (el backend resuelve el alias `greenhouse_nombre`, `sensor_nombre`, `zone_nombre`, `rol_nombre`, ...). El `id` solo se usa internamente para construir la URL de edicion o borrado.

### DataTables

Todas las tablas del sitio usan `datatables.net-bs5` a traves del componente `DataTable`, con busqueda, orden y paginacion en espanol.

---

## Pruebas

Las pruebas no requieren una base de datos real: la capa de conexion se simula y se verifica el SQL generado.

```powershell
.\.venv\Scripts\python.exe -m pytest tests\ -q
```

Cubren:

- Que todo listado filtre por `estado = TRUE`.
- Que el borrado genere `UPDATE ... SET estado = FALSE` y **nunca** `DELETE FROM`.
- Que `require_permission` consulte `moduloxrol` por nombre de rol y rechace con 403.
- Que el asistente rechace sentencias destructivas y que su respuesta no contenga SQL.
- Que los modelos de escritura no acepten `id`.

---

## Despliegue

El proyecto tiene dos piezas que se despliegan por separado en Render:

- **La API** (FastAPI + PostgreSQL en Neon) -> Web Service
- **El frontend** (SvelteKit) -> Static Site
- **La API auxiliar** (Express + MySQL en Aiven) -> Web Service

La base de datos ya esta en Neon, asi que solo se despliega el codigo.

### 1. La API en Render (Web Service)

En <https://dashboard.render.com> → **New → Web Service** → conecta el repositorio.

| Campo | Valor |
|---|---|
| Name | `apigrowapp` (o el que quieras) |
| Root Directory | *(vacio)* |
| Runtime | Python |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| Instance Type | Free (o Starter) |

> **Nunca pongas `--reload` en el Start Command de Render**: es solo para desarrollo local. Con `--reload` Render reinicia el proceso en cada cambio y el servicio se cae.

#### Variables de entorno de la API

En *Environment* del servicio, agrega estas variables (los valores de Neon los copias de *Neon → Dashboard → Connection Details*):

| Variable | Valor | Nota |
|---|---|---|
| `DB_HOST` | `ep-xxxxxxxx-pooler.c-9.us-east-2.aws.neon.tech` | **Usa el host con `-pooler`**: es el que aguanta muchas conexiones |
| `DB_PORT` | `5432` | |
| `DB_NAME` | `neondb` | |
| `DB_USER` | `neondb_owner` | |
| `DB_PASSWORD` | *(la de Neon)* | |
| `DB_SSL` | `true` | Obligatorio en Neon |
| `SECRET_KEY` | *(clave larga y aleatoria)* | Genera una con `python -c "import secrets; print(secrets.token_urlsafe(48))"` |
| `CORS_ORIGINS` | `https://tu-frontend.onrender.com` | Se agrega despues de crear el frontend |
| `DB_POOL_MIN` | `10` | Conexiones precreadas (opcional, valor por defecto 5) |
| `DB_POOL_MAX` | `15` | Conexiones maximas simultaneas (opcional) |

Render lee esas variables desde su panel: **no hace falta el archivo `.env`** en el servidor.

#### Comprobar que la API quedo viva

Abre `https://tu-api.onrender.com/health` → debe responder `{"status":"healthy"}`.
Y `https://tu-api.onrender.com/docs` → la documentacion interactiva.

> **Primer arranque**: Render hace el build la primera vez y tarda unos minutos. Ademas, el plan gratuito se duerme tras 15 minutos sin uso: la primera peticion despues de dormir tarda un poco mas (arranque en frio). El pool de conexiones ya se precalienta al arrancar para que las peticiones siguientes sean rapidas.

### 2. El frontend en Render (Static Site)

En <https://dashboard.render.com> → **New → Static Site** → conecta el mismo repositorio.

| Campo | Valor |
|---|---|
| Name | `growapp` |
| Root Directory | `frontend` |
| Build Command | `npm install && npm run build` |
| Publish Path | `build` |

Agrega en *Environment*:

| Variable | Valor |
|---|---|
| `VITE_API_URL` | `https://tu-api.onrender.com` |

Y en *Settings → Redirects/Headers* agrega la regla de reescritura:

| Source | Destination | Status |
|---|---|---|
| `/*` | `/index.html` | 200 (Rewrite) |

> **Las variables `VITE_*` se leen al compilar**, no al servir. Si cambias `VITE_API_URL`, tienes que guardar y volver a compilar el sitio para que el cambio tome efecto.

La URL publica del frontend te sirve para completar `CORS_ORIGINS` en la API (y volver a desplegar la API si la cambias).

### 3. La API auxiliar (modulos externos)

En Render como otro Web Service con Root Directory `express-api`, Build `npm install`, Start `npm start`, Health Check `/health` y la variable `MYSQL_URL` con el Service URI de Aiven. Despues agrega su URL publica como `VITE_EXPRESS_URL` en el frontend y vuelve a compilarlo.

> **Atajo:** el archivo `render.yaml` de la raiz es un *Blueprint* con las tres piezas. En Render → **New → Blueprint** → elige el repositorio y completa las variables que pide (las de Neon, `MYSQL_URL`, `CORS_ORIGINS`, `VITE_API_URL` y `VITE_EXPRESS_URL`).

### 4. Orden recomendado

1. Despliega la API → anota `https://tu-api.onrender.com`.
2. Despliega el frontend con `VITE_API_URL` = esa URL → anota `https://tu-frontend.onrender.com`.
3. Vuelve a la API y pon `CORS_ORIGINS=https://tu-frontend.onrender.com` → Render la reinicia sola.
4. Abre el frontend, entra con `admin` / `Admin123*` y prueba el Asistente.

### Comprobacion final en produccion

```powershell
curl.exe https://tu-api.onrender.com/health
curl.exe -X POST -d "username=admin&password=Admin123*" https://tu-api.onrender.com/auth/login
curl.exe https://tu-frontend.onrender.com
```

---

## Reglas de negocio implementadas

| Regla | Donde se cumple |
|---|---|
| Windows: sin scripts bash, sin rutas macOS, `python -m ...` | `scripts/`, `requirements.txt`, `app/core/database.py` |
| Minimo 10 componentes reutilizables | `frontend/src/lib/components/` (16) |
| Todas las llamadas a la API centralizadas | `frontend/src/lib/services/` |
| `fetch` prohibido fuera de services | verificacion por grep en `frontend/src/` |
| Proxy `/api` al backend | `frontend/vite.config.js` |
| `bind:value`, `preventDefault()`, `onMount()` | componentes y rutas del frontend |
| Menu funcional y responsive con DataTables | `(app)/+layout.svelte`, `DataTable.svelte` |
| Nunca mostrar IDs | `frontend/src/lib/config/modulos.js` + alias del backend |
| SQL puro con psycopg2, sin ORM | `app/repositories/` |
| Minimo 12 tablas con auditoria y borrado logico | `schema.sql` (16 tablas) |
| JWT y redireccion por rol | `app/core/auth.py`, `moduloxrol` |
| Reflejo de procesos entre roles | matriz de permisos en `moduloxrol` |
| El asistente nunca muestra SQL | `app/core/asistente.py` |
