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
| T1 | S1 | repo raíz | Sanear macOS: borrar `.venv`, `__MACOSX/`, `.DS_Store`, `__pycache__`; `.gitignore` actualizado; `.env.example` raíz; scripts `.ps1`/`.bat`; README Windows |
| T2 | S10, S11, S12, S18 | `schema.sql` | 16 tablas con `creado/actualizado/estado`, triggers de `actualizado`, 10 roles del agro, semillas 20/10, matriz `moduloxrol` |
| T3 | S9, S16 | `app/core/database.py`, `app/repositories/*` | Pool `psycopg2` síncrono, repositorios con SQL puro, sin `DELETE` físico |
| T4 | S11, S12, S13 | `app/api/*`, `app/core/auth.py` | Routers síncronos, permisos por `moduloxrol`,JWT con claim de rol |
| T5 | S9 | `app/models/*` | Pydantic v2, sin `id` en Create/Update, `ConfigDict(from_attributes=True)` |
| T6 | S15 | `app/core/asistente.py`, `app/api/rutas_asistente.py` | `get_schema()`, `run_sql_query()` (solo SELECT), respuesta en lenguaje natural, sin SQL en la salida |
| T7 | S2, S3, S4, S5, S6, S7, S8 | `frontend/` | `svelte.config.js`, proxy `/api`, `src/lib/services/*` por dominio, `bind:value`, `Header.svelte`/`Card.svelte`, rutas limpias |
| T8 | S1..S18 | repo raíz | Verificación: `npm run build` + `svelte-check`, `pytest` de permisos/soft-delete, `compileall` |

## Log

- L1: Petición original del usuario: auditar, adaptar y reestructurar el proyecto que estaba en macOS para que funcione en su PC con Windows, cumpliendo las reglas de negocio de "Taller 1 Corte 2", "Parcial II" y módulos CRUD, con SvelteKit (componentes/services/rutas), FastAPI modular (modelos/repositorios/routers), PostgreSQL en Neon con auditoría y borrado lógico, roles por `moduloxrol`, y un asistente que nunca muestre SQL. Al final: "Espera mi confirmación para proceder con la generación/edición del código."
- L2: Auditoría entregada y confirmada por el usuario. Hallazgos verificados: `.venv` de macOS (`/Library/Frameworks/Python.framework`, `bin/`), `node_modules` con shim POSIX (`node_modules/.bin/svelte-kit` sin `.cmd`) y binario `lightningcss-darwin-x64`, `__MACOSX/` y `.DS_Store`, `frontend/svelte.config.js` ausente con `adapter` mal ubicado dentro de `sveltekit()`, sin `server.proxy`, sin `.env`/`.env.example` raíz, y módulo `estudiantes` huérfano (tabla inexistente + `DELETE FROM estudiantes` físico). Corrección posterior: los imports de `main.py` SÍ resuelven vía los alias de `app/api/__init__.py`.
- L3: Decisiones del usuario: (a) migrar la capa de datos a psycopg2; (b) mantener las dos bases (Neon PostgreSQL + MySQL/Railway con express-api); (c) roles del agro en vez de docente/estudiante, a criterio del implementador; (d) implementar el asistente de consultas a BD.
