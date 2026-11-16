# Port a Windows + reestructuracion del Invernadero Inteligente (GrowApp)

Feature: `port-windows`
Estado: en curso
Objetivo: que el proyecto funcione en Windows (SvelteKit + FastAPI + PostgreSQL Neon) cumpliendo las reglas de negocio del taller.

## Specs

- S1: "Revisa package.json, .env y scripts de Python. Ajusta rutas (usa \\ o path.join), comandos (python vs python3) y elimina dependencias de scripts bash."
- S2: "src/lib/components: Mínimo 10 componentes reutilizables (ej. Navbar.svelte, Footer.svelte, Header.svelte, Card.svelte)."
- S3: "src/lib/services: Centraliza TODAS las llamadas a la API (ej. api_estudiante.js). Prohibido usar fetch directamente en las rutas (+page.svelte)."
- S4: "src/routes: Uso estricto de +layout.svelte y +page.svelte."
- S5: "Proxy: vite.config.js debe tener configurado el proxy para redirigir /api al backend (ej. http://localhost:8000)."
- S6: "Formularios: Usa bind:value para capturar datos, preventDefault() en envíos y onMount() para carga inicial."
- S7: "Interfaz: Menú de navegación 100% funcional. Plantilla responsive con colores acordes. Uso de DataTables en todas las tablas."
- S8: "Regla estricta de UI: En NINGÚN módulo el usuario debe ver IDs de la base de datos ni campos para insertar/editar IDs."
- S9: "Arquitectura modular (FastAPI): Estructura en app/api, app/core (database), app/models (Pydantic), y app/repositories (SQL puro con psycopg2)."
- S10: "Base de datos principal (mínimo 12 tablas, 20 registros principales, 10 secundarios)."
- S11: "TODAS las tablas deben tener obligatoriamente los campos: creado (fecha/hora de creación), actualizado (fecha/hora de modificación) y estado (booleano o numérico 1/0 para borrado lógico). El borrado físico está prohibido."
- S12: "Tablas obligatorias: rol, usuario, modulo, moduloxrol."
- S13: "Autenticación y Roles: Implementar JWT en el login. Cada rol (ej. Docente, Estudiante, Administrador) debe ser redirigido SOLO a los módulos permitidos según la tabla moduloxrol."
- S14: "Reflejo de procesos: El CRUD completo debe reflejar cambios entre roles (ej. lo que registra un docente lo ve un estudiante)."
- S15: "Regla Absoluta de IA: Si se integra un asistente para consultas BD, este NUNCA debe mostrar código SQL al usuario. Debe usar get_schema(), ejecutar con run_sql_query() y responder solo con el resultado en lenguaje natural."
- S16: "Migrar a psycopg2" (decisión del usuario sobre el driver de base de datos).
- S17: "Mantener las dos bases" (decisión del usuario: PostgreSQL/Neon + MySQL/Railway vía express-api).
- S18: Roles del dominio acordados por el usuario: no roles docente/estudiante; roles del agro del invernadero (administrador, supervisor, agronomo, regador, tecnico, auxiliar_riego, planificador, calidad, mantenimiento, lector).

## Tasks

| ID | Specs | Ruta | Entrega |
|----|-------|------|---------|
| T1 | S1 | repo raíz | Sanear macOS: borrar `.venv`, `__MACOSX/`, `.DS_Store`, `__pycache__`, `node_modules` darwin; `.gitignore` actualizado; `.env.example` raíz; scripts `.ps1`/`.bat`; README Windows |
| T2 | S10, S11, S12, S18 | `schema.sql` | 16 tablas con `creado/actualizado/estado`, triggers de `actualizado`, 10 roles del agro, semillas 20/10, matriz `moduloxrol` |
| T3 | S9, S16 | `app/core/database.py`, `app/repositories/*` | Pool `psycopg2` síncrono, repositorios con SQL puro, sin `DELETE` físico |
| T4 | S11, S12, S13 | `app/api/*`, `app/core/auth.py` | Routers síncronos, permisos por `moduloxrol`,JWT con claim de rol |
| T5 | S9 | `app/models/*` | Pydantic v2, sin `id` en Create/Update, `ConfigDict(from_attributes=True)` |
| T6 | S15 | `app/core/asistente.py`, `app/api/rutas_asistente.py` | `get_schema()`, `run_sql_query()` (solo SELECT), respuesta en lenguaje natural, sin SQL en la salida |
| T7 | S2, S3, S4, S5, S6, S7, S8 | `frontend/` | `svelte.config.js`, proxy `/api`, `src/lib/services/*` por dominio, `bind:value`, `Header.svelte`/`Card.svelte`, rutas limpias |
| T8 | S1..S18 | repo raíz | Verificación: `npm run build` + `svelte-check`, `pytest` de permisos/soft-delete, `compileall` |

## Commits

| Commit | Unidad |
|--------|--------|
| 724af55 | Baseline del proyecto migrado desde macOS |
| 5ce9205 | Guia de instalacion y ejecucion en Windows |
| 7f0d813 | Esquema PostgreSQL con 16 tablas auditadas y matriz de permisos |
| 3ab4f9c | Backend sobre psycopg2 con SQL puro y routers sincronos |
| e9c2160 | Frontend: capa de servicios, proxy /api y SPA funcional |
| 4d16ecf | Correcciones del pool, del filtro por id y del alias de sensores |
| c5d995e | Limpieza del respaldo del esquema |

## Log

- L1: Petición original del usuario: auditar, adaptar y reestructurar el proyecto que estaba en macOS para que funcione en su PC con Windows, cumpliendo las reglas de negocio de "Taller 1 Corte 2", "Parcial II" y módulos CRUD, con SvelteKit (componentes/services/rutas), FastAPI modular (modelos/repositorios/routers), PostgreSQL en Neon con auditoría y borrado lógico, roles por `moduloxrol`, y un asistente que nunca muestre SQL. Al final: "Espera mi confirmación para proceder con la generación/edición del código."
- L2: Auditoría entregada y confirmada por el usuario. Hallazgos verificados: `.venv` de macOS (`/Library/Frameworks/Python.framework`, `bin/`), `node_modules` con shim POSIX (`node_modules/.bin/svelte-kit` sin `.cmd`) y binario `lightningcss-darwin-x64`, `__MACOSX/` y `.DS_Store`, `frontend/svelte.config.js` ausente con `adapter` mal ubicado dentro de `sveltekit()`, sin `server.proxy`, sin `.env`/`.env.example` raíz, y módulo `estudiantes` huérfano (tabla inexistente + `DELETE FROM estudiantes` físico). Corrección posterior: los imports de `main.py` SÍ resuelven vía los alias de `app/api/__init__.py`.
- L3: Decisiones del usuario: (a) migrar la capa de datos a psycopg2; (b) mantener las las dos bases (Neon PostgreSQL + MySQL/Railway con express-api); (c) roles del agro en vez de docente/estudiante, a criterio del implementador; (d) implementar el asistente de consultas a BD.
- L4: Se inicializo git en la carpeta del proyecto (no venia con repositorio) sobre la rama `feature/port-windows`, con un commit baseline `724af55` que deja constancia del estado migrado desde macOS. Los commits son locales: no se hace push sin decision del usuario.
- L5: T1 completada: eliminados `.venv` (macOS), `__MACOSX/`, `.DS_Store`, `__pycache__/` y `frontend/node_modules` (shims POSIX `svelte-kit` sin `.cmd` y binario `lightningcss-darwin-x64`); creados `.gitignore`, `.env.example` (raiz), `frontend/.env.example`, `express-api/.env.example`, seis scripts Windows (`instalar_dependencias.ps1`, `iniciar_api.ps1|.bat`, `iniciar_frontend.ps1|.bat`, `iniciar_api_express.ps1`) y README reescrito con guia de instalacion Windows.
- L6: T2, T3+T5, T6 y T7 se ejecutan en paralelo con tres writers de superficies disjuntas: `schema.sql`; `app/`+`main.py`+`requirements.txt`+`tests/`; `frontend/`. Contrato compartido fijado en el prompt de cada writer (16 tablas, 10 roles del agro, 16 modulos, endpoints y alias de relaciones).
- L7: Verificacion independiente del padre (no declarada por los writers): `schema.sql` ejecutado COMPLETO en un PostgreSQL 16 real (portable, sin sudo) -> 16 tablas creadas y sembradas; `sqlglot` parsea las 135 sentencias sin error. Cruce de los INSERT de los repositorios contra las columnas reales del esquema: 0 discrepancias. `pytest` -> 113 passed. `compileall` -> exit 0. `npm run build` -> exit 0 y `npm run check` -> 0 errores 0 warnings.
- L8: Prueba end-to-end con PostgreSQL real + Uvicorn + Vite dev + navegador: login JWT real (`admin`), `/auth/modulos` devuelve 16 modulos para administrador y 8 para lector, `lector` recibe 403 al crear un cultivo y al entrar a `irrigation-zones`, `regador` crea una zona de riego y el `lector` ve despues ese registro en el historial (reflejo entre roles), el borrado deja la fila con `estado = FALSE` y la API ya no la lista, y el asistente responde solo con texto en espanol.
- L9: Tres defectos encontrados y corregidos durante esa prueba, con test de regresion en cada caso: (a) `ThreadedConnectionPool.getconn()` no espera y el panel carga 16 modulos en paralelo, lo que agotaba el pool y devolvia 503 -> semaforo de turnos con `DB_POOL_TIMEOUT`; (b) el asistente filtraba el invernadero solo por nombre, asi que 'el invernadero 1' no encontraba sensores -> ahora un invernadero numerado se busca por id y se responde con su nombre; (c) el listado de sensores no traia el alias `greenhouse_nombre` como el resto de modulos -> JOIN agregado. Ademas se corrigio el plural de las respuestas del asistente ('1 sensor', '10 estudiantes').
- L10: Ajuste propio del padre sobre lo entregado por el writer de frontend: `config.js` ahora usa `VITE_API_URL`/`VITE_EXPRESS_URL` cuando estan definidas, porque en un despliegue estatico no hay proxy de Vite y `/api` relativo no llegaria al backend. El `.env.example` del frontend se actualizo en consecuencia.
- L11: Commits de unidad de trabajo en la rama `feature/port-windows`: 724af55 baseline, 5ce9205 README Windows, 7f0d813 esquema, 3ab4f9c backend psycopg2, e9c2160 frontend, 4d16ecf correcciones de pool y asistente, c5d995e limpieza. Sin push: la publicacion es decision del usuario.
- L12: Pendiente para el usuario en su PC Windows: crear `.env` con las credenciales de Neon, ejecutar `npm install` en `frontend/` (el `node_modules` actual es de Linux) y cargar `schema.sql` en la base de datos. La API auxiliar Express + MySQL no se pudo ejecutar en esta maquina (no hay MySQL): su codigo y su `schema.sql` quedaron intactos.
