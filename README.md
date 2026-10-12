# Grow A Garden API

API REST para la gestion de jardines y cultivos inteligentes con FastAPI y PostgreSQL.

## Tabla de Contenidos

1. [Autores](#autores)
2. [URLs Desplegadas](#urls-desplegadas)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Arquitectura](#arquitectura)
   - [API Principal (FastAPI + PostgreSQL)](#api-principal-fastapi--postgresql)
   - [API Auxiliar (Express + MySQL)](#api-auxiliar-express--mysql)
   - [Dashboard Web](#dashboard-web)
5. [Base de Datos Principal (PostgreSQL - Neon)](#base-de-datos-principal-postgresql---neon)
   - [Tablas de Negocio (14 tablas)](#tablas-de-negocio-14-tablas)
   - [Tablas RBAC (4 tablas)](#tablas-rbac-4-tablas)
   - [Campos Obligatorios](#campos-obligatorios-en-todas-las-tablas)
6. [Base de Datos Auxiliar (MySQL - Railway)](#base-de-datos-auxiliar-mysql---railway)
   - [Tablas (3 tablas)](#tablas-3-tablas)
7. [Autenticacion y Autorizacion](#autenticacion-y-autorizacion)
   - [JWT (API Principal)](#jwt-api-principal)
   - [Permisos RBAC](#permisos-rbac)
8. [Endpoints Principales (FastAPI)](#endpoints-principales-fastapi)
   - [Auth](#auth)
   - [Greenhouses](#greenhouses)
   - [Sensors](#sensors)
   - [Sensor Readings](#sensor-readings)
   - [Crops](#crops)
   - [Crop Batches](#crop-batches)
   - [Users](#users)
   - [Alerts](#alerts)
   - [Irrigation Zones](#irrigation-zones)
   - [Irrigation Logs](#irrigation-logs)
   - [Actuators](#actuators)
   - [Actuator Controls](#actuator-controls)
   - [Greenhouse Settings](#greenhouse-settings)
9. [Endpoints Auxiliares (Express)](#endpoints-auxiliares-express)
10. [Despliegue](#despliegue)
    - [Render.com](#rendercom)
    - [Railway.app](#railwayapp)
    - [Variables de Entorno](#variables-de-entorno)
11. [Tech Stack](#tech-stack)

---

## Autores

- Esteban Gomez Jimenez
- Victor Daniel Amaranto Garizabalo

## URLs Desplegadas

- **API Principal:** https://apigrowapp.onrender.com
- **API Auxiliar:** https://apigrowappexpress.onrender.com
- **Web Dashboard:** https://webpage-56vp.onrender.com

## Estructura del Proyecto

```
api2026/
├── app/                          # FastAPI Application (API Principal)
│   ├── api/                      # Route handlers
│   │   ├── rutas_auth.py
│   │   ├── rutas_greenhouse.py
│   │   ├── rutas_sensor.py
│   │   ├── rutas_sensor_reading.py
│   │   ├── rutas_crop.py
│   │   ├── rutas_crop_batch.py
│   │   ├── rutas_user.py
│   │   ├── rutas_alert.py
│   │   ├── rutas_irrigation_zone.py
│   │   ├── rutas_irrigation_log.py
│   │   ├── rutas_actuator.py
│   │   ├── rutas_actuator_control.py
│   │   └── rutas_greenhouse_setting.py
│   ├── core/
│   │   ├── auth.py               # JWT authentication
│   │   └── database.py           # asyncpg connection pool
│   ├── models/                   # Pydantic models
│   └── repositories/             # Database access layer
├── express-api/                  # Express.js API (API Auxiliar)
│   ├── src/
│   │   ├── index.js              # Entry point
│   │   ├── config/
│   │   │   └── database.js       # MySQL connection pool
│   │   ├── routes/
│   │   │   ├── sensores.js       # /sensores-externos
│   │   │   ├── lecturas.js       # /lecturas-externas
│   │   │   └── alertas.js       # /alertas-externas
│   │   └── middleware/
│   │       └── errorHandler.js
│   └── schema.sql                # MySQL schema
├── web/                          # Web Dashboard
├── docs/                         # Documentation
├── main.py                       # FastAPI entry point
├── schema.sql                    # PostgreSQL schema
└── requirements.txt              # Python dependencies
```

## Arquitectura

### API Principal (FastAPI + PostgreSQL)

La API principal esta construida con FastAPI y se conecta a una base de datos PostgreSQL hospedada en Neon. Esta API maneja toda la logica de negocio relacionada con la gestion de areas de cultivo, sensores, cultivos, alertas y actuadores.

**Tecnologias:**
- FastAPI (Python 3.11+)
- PostgreSQL (Neon)
- asyncpg (conexion asincrona)
- Pydantic v2 (validacion)
- python-jose (JWT)
- bcrypt (hash de contrasenas)
- Uvicorn (servidor)

### API Auxiliar (Express + MySQL)

La API auxiliar esta construida con Express.js y se conecta a una base de datos MySQL Hospedada en Railway. Esta API maneja sensores externos, lecturas externas y alertas externas.

**Tecnologias:**
- Express.js (Node.js)
- MySQL (Railway)
- mysql2 (driver)
- CORS
- dotenv

### Dashboard Web

Interfaz de usuario construida con JavaScript vanilla y CSS. Se comunica con la API principal para mostrar y gestionar los datos del sistema.

## Base de Datos Principal (PostgreSQL - Neon)

### Tablas de Negocio (14 tablas)

| Tabla | Descripcion |
|-------|-------------|
| greenhouses | Areas de cultivo del sistema |
| sensors | Sensores de monitoreo |
| sensor_readings | Lecturas de sensores |
| crops | Catalogo de cultivos |
| crop_batches | Lotes de cultivos |
| alerts | Alertas del sistema |
| irrigation_zones | Zonas de riego |
| irrigation_logs | Historial de riego |
| actuators | Actuadores |
| actuator_controls | Control de actuadores |
| greenhouse_settings | Configuraciones de area de cultivo |
| sensores_externos | Sensores externos |
| lecturas_externas | Lecturas externas |
| alertas_externas | Alertas externas |

### Tablas RBAC (4 tablas)

| Tabla | Descripcion |
|-------|-------------|
| rol | Roles del sistema (administrador, operador, readonly) |
| modulo | Modulos del sistema |
| moduloxrol | Permisos por rol y modulo |
| usuario | Usuarios del sistema |

### Campos Obligatorios en Todas las Tablas

Todas las tablas de la base de datos incluyen los siguientes campos de auditoria:

- **estado**: BOOLEAN DEFAULT TRUE - Para eliminacion logica (soft delete)
- **creado**: TIMESTAMP DEFAULT CURRENT_TIMESTAMP - Fecha de creacion del registro
- **actualizado**: TIMESTAMP DEFAULT CURRENT_TIMESTAMP - Fecha de ultima modificacion

## Base de Datos Auxiliar (MySQL - Railway)

### Tablas (3 tablas)

| Tabla | Descripcion |
|-------|-------------|
| sensores_externos | Sensores externos de monitoreo |
| lecturas_externas | Lecturas de sensores externos |
| alertas_externas | Alertas generadas por sensores externos |

Todas las tablas incluyen los campos obligatorios: estado, creado, actualizado.

## Autenticacion y Autorizacion

### JWT (API Principal)

El sistema de autenticacion de la API principal utiliza JWT (JSON Web Tokens):

- Algoritmo: HS256
- Tiempo de expiracion: 24 horas
- Almacenamiento: localStorage en el frontend
- Encabezado: Authorization: Bearer <token>

### Permisos RBAC

El sistema implementa control de acceso basado en roles:

| Rol | Permisos |
|-----|----------|
| administrador | CRUD completo en todos los modulos |
| operador | CRUD en modulos de operacion, lectura en otros |
| readonly | Solo lectura en todos los modulos |

## Endpoints Principales (FastAPI)

### Auth

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| POST | /auth/login | Iniciar sesion |
| POST | /auth/register | Registrar usuario |
| GET | /auth/me | Obtener usuario actual |

### Greenhouses

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | /greenhouses | Listar areas de cultivo |
| GET | /greenhouses/{greenhouse_id} | Obtener area de cultivo |
| POST | /greenhouses | Crear area de cultivo |
| PUT | /greenhouses/{greenhouse_id} | Actualizar area de cultivo |
| DELETE | /greenhouses/{greenhouse_id} | Eliminar area de cultivo |

### Sensors

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | /sensors | Listar sensores |
| GET | /sensors/{sensor_id} | Obtener sensor |
| GET | /sensors/greenhouse/{greenhouse_id} | Sensores por area de cultivo |
| POST | /sensors | Crear sensor |
| PUT | /sensors/{sensor_id} | Actualizar sensor |
| DELETE | /sensors/{sensor_id} | Eliminar sensor |

### Sensor Readings

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | /sensor-readings | Listar lecturas |
| GET | /sensor-readings/{reading_id} | Obtener lectura |
| GET | /sensor-readings/sensor/{sensor_id} | Lecturas por sensor |
| GET | /sensor-readings/greenhouse/{greenhouse_id}/latest | Ultima lectura por area de cultivo |
| POST | /sensor-readings | Crear lectura |

### Crops

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | /crops | Listar cultivos |
| GET | /crops/{crop_id} | Obtener cultivo |
| POST | /crops | Crear cultivo |
| PUT | /crops/{crop_id} | Actualizar cultivo |
| DELETE | /crops/{crop_id} | Eliminar cultivo |

### Crop Batches

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | /crop-batches | Listar lotes |
| GET | /crop-batches/{batch_id} | Obtener lote |
| GET | /crop-batches/greenhouse/{greenhouse_id} | Lotes por area de cultivo |
| POST | /crop-batches | Crear lote |
| PUT | /crop-batches/{batch_id} | Actualizar lote |
| DELETE | /crop-batches/{batch_id} | Eliminar lote |

### Users

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | /users | Listar usuarios |
| GET | /users/{user_id} | Obtener usuario |
| GET | /users/username/{username} | Obtener por username |
| POST | /users | Crear usuario |
| PUT | /users/{user_id} | Actualizar usuario |
| DELETE | /users/{user_id} | Eliminar usuario |

### Alerts

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | /alerts | Listar alertas |
| GET | /alerts/activas | Alertas activas |
| GET | /alerts/{alert_id} | Obtener alerta |
| POST | /alerts | Crear alerta |
| PATCH | /alerts/{alert_id}/resolver | Resolver alerta |
| PATCH | /alerts/{alert_id}/reconocer | Reconocer alerta |

### Irrigation Zones

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | /irrigation-zones | Listar zonas |
| GET | /irrigation-zones/{zone_id} | Obtener zona |
| GET | /irrigation-zones/greenhouse/{greenhouse_id} | Zonas por area de cultivo |
| POST | /irrigation-zones | Crear zona |
| PUT | /irrigation-zones/{zone_id} | Actualizar zona |
| DELETE | /irrigation-zones/{zone_id} | Eliminar zona |

### Irrigation Logs

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | /irrigation-logs | Listar registros |
| GET | /irrigation-logs/{log_id} | Obtener registro |
| GET | /irrigation-logs/zone/{zone_id} | Registros por zona |
| POST | /irrigation-logs | Crear registro |

### Actuators

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | /actuators | Listar actuadores |
| GET | /actuators/{actuator_id} | Obtener actuador |
| GET | /actuators/greenhouse/{greenhouse_id} | Actuadores por area de cultivo |
| POST | /actuators | Crear actuador |
| PUT | /actuators/{actuator_id} | Actualizar actuador |
| DELETE | /actuators/{actuator_id} | Eliminar actuador |

### Actuator Controls

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | /actuator-controls | Listar controles |
| GET | /actuator-controls/{control_id} | Obtener control |
| GET | /actuator-controls/actuator/{actuator_id} | Controles por actuador |
| POST | /actuator-controls | Crear control |

### Greenhouse Settings

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | /greenhouse-settings | Listar configuraciones |
| GET | /greenhouse-settings/{setting_id} | Obtener configuracion |
| GET | /greenhouse-settings/greenhouse/{greenhouse_id} | Config por area de cultivo |
| POST | /greenhouse-settings | Crear configuracion |
| PUT | /greenhouse-settings/greenhouse/{greenhouse_id} | Actualizar configuracion |

## Endpoints Auxiliares (Express)

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | / | Raiz de la API |
| GET | /health | Estado de salud |
| GET | /sensores-externos | Listar sensores externos |
| GET | /sensores-externos/:id | Obtener sensor por ID |
| POST | /sensores-externos | Crear sensor |
| PUT | /sensores-externos/:id | Actualizar sensor |
| DELETE | /sensores-externos/:id | Eliminar sensor (soft delete) |
| GET | /lecturas-externas | Listar lecturas |
| POST | /lecturas-externas | Crear lectura |
| GET | /alertas-externas | Listar alertas |
| POST | /alertas-externas | Crear alerta |
| PUT | /alertas-externas/:id | Actualizar alerta |
| DELETE | /alertas-externas/:id | Eliminar alerta (soft delete) |

## Despliegue

### Render.com

Ambos servicios API estan desplegados en Render.com:
- API Principal: Servicio web con Uvicorn
- API Auxiliar: Servicio web con Node.js

### Railway.app

La base de datos MySQL esta hospedada en Railway con conexion publica habilitada.

### Variables de Entorno

**API Principal (Neon PostgreSQL):**
- DB_HOST
- DB_NAME
- DB_USER
- DB_PASSWORD
- DB_PORT

**API Auxiliar (Railway MySQL):**
- MYSQL_URL: mysql://root:password@host:puerto/database
- PORT: 3000

**Nota:** Las credenciales reales se configuran en los servicios de despliegue y no se almacenan en el repositorio.

## Tech Stack

- FastAPI + PostgreSQL (Neon)
- Express + MySQL (Railway)
- JWT Authentication
- Render (despliegue)
- Pydantic (validacion de datos)
- bcrypt (seguridad de contrasenas)
- asyncpg (conexion PostgreSQL asincrona)
- mysql2 (driver MySQL)
