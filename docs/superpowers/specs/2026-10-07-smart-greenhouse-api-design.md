# Smart Greenhouse API - Diseño Técnico

## 1. Resumen del Proyecto

**Nombre:** Smart Greenhouse API  
**Autores:** Esteban Gomez Jimenez, Victor Daniel Amaranto Garizabalo  
**Fecha:** 2026-10-07  
**Descripción:** Sistema de gestión de invernaderos inteligentes con API principal FastAPI/PostgreSQL y API auxiliar Express/MySQL.

---

## 2. FastAPI + PostgreSQL (60%)

### 2.1 Base de Datos Normalizada

**12+ tablas core:**

| Tabla | Descripción |
|-------|-------------|
| `greenhouses` | Invernaderos |
| `sensors` | Sensores |
| `sensor_readings` | Lecturas de sensores |
| `crops` | Catálogo de cultivos |
| `crop_batches` | Lotes de cultivos |
| `users` | Usuarios |
| `alerts` | Alertas |
| `irrigation_zones` | Zonas de riego |
| `irrigation_logs` | Historial de riego |
| `actuators` | Actuadores |
| `actuator_controls` | Control de actuadores |
| `greenhouse_settings` | Configuraciones |

**4 tablas RBAC:**

| Tabla | Descripción |
|-------|-------------|
| `rol` | Roles del sistema |
| `modulo` | Módulos del API |
| `moduloxrol` | Permisos rol-módulo |
| `usuario` | Usuarios (vinculados a rol) |

### 2.2 Estructura de Campos Obligatorios

Todas las tablas deben incluir:

```sql
id SERIAL PRIMARY KEY,
estado BOOLEAN DEFAULT TRUE,        -- 1=activo, 0=eliminado (soft delete)
creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

**Campos únicos:** `username`, `email` en tabla `usuario`.

### 2.3 API Endpoints

**Autenticación JWT:**
- `POST /auth/login` → `{ username, password }` → `{ access_token, token_type }`
- `POST /auth/register` → `{ username, email, password, nombre, rol_id }`
- `GET /auth/me` → usuario actual (protegido)

**CRUD por cada tabla** con endpoints típicos:
- `GET /recurso` → listar todos
- `GET /recurso/{id}` → obtener uno
- `POST /recurso` → crear
- `PUT /recurso/{id}` → actualizar
- `DELETE /recurso/{id}` → soft delete (estado=FALSE)

### 2.4 JWT y Validación

- Librería: `python-jose`
- Algoritmo: `HS256`
- Expiración: 24 horas
- Middleware de validación en rutas protegidas

---

## 3. Express + MySQL (30%)

### 3.1 Base de Datos Auxiliar

**3+ tablas:**

| Tabla | Descripción |
|-------|-------------|
| `sensores_externos` | Sensores externos |
| `lecturas_externas` | Lecturas externas |
| `alertas_externas` | Alertas externas |

**Campos obligatorios:** `id`, `estado BOOLEAN`, `creado`, `actualizado`.

### 3.2 API Endpoints

- `GET /health` → estado del servidor
- `GET /sensores-externos` → listar
- `POST /sensores-externos` → crear
- `GET /lecturas-externas` → listar
- `POST /lecturas-externas` → crear
- `GET /alertas-externas` → listar
- `POST /alertas-externas` → crear

---

## 4. Documentación (10%)

**Resumen de la propuesta** incluyendo:
- Problema: monitoreo y control de invernaderos inteligentes
- Población: agricultores y operadores de invernaderos
- Requerimientos generales del sistema

---

## 5. Stack Tecnológico

| Componente | Tecnología |
|------------|------------|
| API Principal | FastAPI + PostgreSQL (Neon) |
| API Auxiliar | Express + MySQL (PlanetScale) |
| Auth | JWT con python-jose |
| Despliegue | Render |

---

## 6. Estructura de Archivos

```
api2026/
├── app/                    # FastAPI
│   ├── core/
│   │   ├── database.py
│   │   └── auth.py
│   ├── models/
│   ├── repositories/
│   ├── api/
│   └── main.py
├── schema.sql              # PostgreSQL
├── express-api/            # Express + MySQL
│   ├── src/
│   └── package.json
├── docs/
│   └── resumen_propuesta.md
└── requirements.txt
```
