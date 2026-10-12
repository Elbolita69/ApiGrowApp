# Smart Greenhouse API

API REST para la gestion de invernaderos inteligentes con FastAPI y PostgreSQL.

## Autores

- Esteban Gomez Jimenez
- Victor Daniel Amaranto Garizabalo

## URLs Desplegadas

- **API FastAPI:** https://apigrowapp.onrender.com
- **Express API:** https://apigrowappexpress.onrender.com
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
│   │   │   └── alertas.js        # /alertas-externas
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

La API principal esta construida con FastAPI y se conecta a una base de datos PostgreSQL hospedada en Neon. Esta API maneja toda la logica de negocio relacionada con la gestion de invernaderos, sensores, cultivos, alertas y actuadores.

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

Interfaz de usuario construida con JavaScript vanilla y CSS. Se comunica con la API FastAPI para mostrar y gestionar los datos del sistema.

## Base de Datos Principal (PostgreSQL - Neon)

### Tablas de Negocio (14 tablas)

| Tabla | Descripcion |
|-------|-------------|
| greenhouses | Invernaderos del sistema |
| sensors | Sensores de monitoreo |
| sensor_readings | Lecturas de sensores |
| crops | Catalogo de cultivos |
| crop_batches | Lotes de cultivos |
| alerts | Alertas del sistema |
| irrigation_zones | Zonas de riego |
| irrigation_logs | Historial de riego |
| actuators | Actuadores |
| actuator_controls | Control de actuadores |
| greenhouse_settings | Configuraciones de invernadero |
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

El sistema de autenticacion de la API FastAPI utiliza JWT (JSON Web Tokens):

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
| GET | /greenhouses | Listar invernaderos |
| GET | /greenhouses/{greenhouse_id} | Obtener invernadero |
| POST | /greenhouses | Crear invernadero |
| PUT | /greenhouses/{greenhouse_id} | Actualizar invernadero |
| DELETE | /greenhouses/{greenhouse_id} | Eliminar invernadero |

### Sensors

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | /sensors | Listar sensores |
| GET | /sensors/{sensor_id} | Obtener sensor |
| GET | /sensors/greenhouse/{greenhouse_id} | Sensores por invernadero |
| POST | /sensors | Crear sensor |
| PUT | /sensors/{sensor_id} | Actualizar sensor |
| DELETE | /sensors/{sensor_id} | Eliminar sensor |

### Sensor Readings

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | /sensor-readings | Listar lecturas |
| GET | /sensor-readings/{reading_id} | Obtener lectura |
| GET | /sensor-readings/sensor/{sensor_id} | Lecturas por sensor |
| GET | /sensor-readings/greenhouse/{greenhouse_id}/latest | Ultima lectura por invernadero |
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
| GET | /crop-batches/greenhouse/{greenhouse_id} | Lotes por invernadero |
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
| GET | /irrigation-zones/greenhouse/{greenhouse_id} | Zonas por invernadero |
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
| GET | /actuators/greenhouse/{greenhouse_id} | Actuadores por invernadero |
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
| GET | /greenhouse-settings/greenhouse/{greenhouse_id} | Config por invernadero |
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
- API FastAPI: Servicio web con Uvicorn
- API Express: Servicio web con Node.js

### Railway.app

La base de datos MySQL esta hospedada en Railway con conexion publica habilitada.

### Variables de Entorno

**API FastAPI:**
- DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT

**API Express:**
- MYSQL_URL: mysql://root:password@turntable.proxy.rlwy.net:59812/railway
- PORT: 3000

## Tech Stack

- FastAPI + PostgreSQL (Neon)
- Express + MySQL (Railway)
- JWT Authentication
- Render (despliegue)
- Pydantic (validacion de datos)
- bcrypt (seguridad de contrasenas)
- asyncpg (conexion PostgreSQL asincrona)
- mysql2 (driver MySQL)
