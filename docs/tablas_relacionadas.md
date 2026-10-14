# Tablas Relacionadas - Grow A Garden API

> **Nota:** Este documento presenta las relaciones entre tablas de la base de datos en formato de tablas impresas, tal como solicitado. No es un diagrama ER.

---

## 1. TABLAS PRINCIPALES DEL SISTEMA

| # | Nombre de Tabla | Descripción |
|---|-----------------|-------------|
| 1 | `rol` | Roles del sistema (administrador, operador, readonly) |
| 2 | `modulo` | Módulos del sistema |
| 3 | `moduloxrol` | Relación muchos a muchos entre roles y módulos |
| 4 | `usuario` | Usuarios del sistema |
| 5 | `greenhouses` | Invernaderos |
| 6 | `sensors` | Sensores |
| 7 | `sensor_readings` | Lecturas de sensores |
| 8 | `crops` | Catálogo de cultivos |
| 9 | `crop_batches` | Lotes de cultivos |
| 10 | `alerts` | Alertas |
| 11 | `irrigation_zones` | Zonas de riego |
| 12 | `irrigation_logs` | Historial de riego |
| 13 | `actuators` | Actuadores |
| 14 | `actuator_controls` | Control de actuadores |
| 15 | `greenhouse_settings` | Configuraciones de invernaderos |
| 16 | `sensores_externos` | Sensores externos |
| 17 | `lecturas_externas` | Lecturas de sensores externos |
| 18 | `alertas_externas` | Alertas externas |

---

## 2. RELACIONES POR TABLA

### 2.1 Tabla: `rol`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | SERIAL (PK) | Identificador único del rol |
| nombre | VARCHAR(50) | Nombre del rol |
| descripcion | VARCHAR(200) | Descripción del rol |
| estado | BOOLEAN | Estado del rol |

**Relaciones:**

| Tabla Relacionada | Tipo de Relación | Campo FK | Cardinalidad |
|-------------------|------------------|----------|--------------|
| `usuario` | 1:N | `usuario.rol_id` | Un rol puede tener muchos usuarios |
| `moduloxrol` | 1:N | `moduloxrol.rol_id` | Un rol puede tener muchos permisos de módulo |

---

### 2.2 Tabla: `modulo`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | SERIAL (PK) | Identificador único del módulo |
| nombre | VARCHAR(100) | Nombre del módulo |
| descripcion | VARCHAR(200) | Descripción del módulo |
| estado | BOOLEAN | Estado del módulo |

**Relaciones:**

| Tabla Relacionada | Tipo de Relación | Campo FK | Cardinalidad |
|-------------------|------------------|----------|--------------|
| `moduloxrol` | 1:N | `moduloxrol.modulo_id` | Un módulo puede tener muchos permisos por rol |

---

### 2.3 Tabla: `moduloxrol` (Tabla Pivote)
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | SERIAL (PK) | Identificador único |
| rol_id | INTEGER (FK) | Referencia a `rol.id` |
| modulo_id | INTEGER (FK) | Referencia a `modulo.id` |
| puede_ver | BOOLEAN | Permiso de visualización |
| puede_crear | BOOLEAN | Permiso de creación |
| puede_editar | BOOLEAN | Permiso de edición |
| puede_eliminar | BOOLEAN | Permiso de eliminación |

**Relaciones:**

| Tabla Relacionada | Tipo de Relación | Campo FK | Cardinalidad |
|-------------------|------------------|----------|--------------|
| `rol` | N:1 | `rol_id` → `rol.id` | Muchos permisos pertenecen a un rol |
| `modulo` | N:1 | `modulo_id` → `modulo.id` | Muchos permisos pertenecen a un módulo |

**Clave Única:** `UNIQUE(rol_id, modulo_id)` - Un rol no puede tener el mismo módulo dos veces

---

### 2.4 Tabla: `greenhouses`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | SERIAL (PK) | Identificador único del invernadero |
| nombre | VARCHAR(100) | Nombre del invernadero |
| ubicacion | VARCHAR(200) | Ubicación física |
| area_metros_cuadrados | NUMERIC(10,2) | Área en metros cuadrados |
| capacidad_maxima | INTEGER | Capacidad máxima de plantas |
| estado | BOOLEAN | Estado del invernadero |

**Relaciones:**

| Tabla Relacionada | Tipo de Relación | Campo FK | Cardinalidad |
|-------------------|------------------|----------|--------------|
| `sensors` | 1:N | `sensors.greenhouse_id` | Un invernadero puede tener muchos sensores |
| `crop_batches` | 1:N | `crop_batches.greenhouse_id` | Un invernadero puede tener muchos lotes de cultivos |
| `alerts` | 1:N | `alerts.greenhouse_id` | Un invernadero puede tener muchas alertas |
| `irrigation_zones` | 1:N | `irrigation_zones.greenhouse_id` | Un invernadero puede tener muchas zonas de riego |
| `actuators` | 1:N | `actuators.greenhouse_id` | Un invernadero puede tener muchos actuadores |
| `greenhouse_settings` | 1:1 | `greenhouse_settings.greenhouse_id` | Un invernadero tiene una configuración única |

---

### 2.5 Tabla: `usuario`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | SERIAL (PK) | Identificador único del usuario |
| username | VARCHAR(50) | Nombre de usuario |
| email | VARCHAR(100) | Correo electrónico |
| password_hash | VARCHAR(255) | Contraseña encriptada |
| nombre | VARCHAR(100) | Nombre completo |
| rol_id | INTEGER (FK) | Referencia a `rol.id` |
| estado | BOOLEAN | Estado del usuario |

**Relaciones:**

| Tabla Relacionada | Tipo de Relación | Campo FK | Cardinalidad |
|-------------------|------------------|----------|--------------|
| `rol` | N:1 | `rol_id` → `rol.id` | Muchos usuarios pueden tener el mismo rol |
| `actuator_controls` | 1:N | `actuator_controls.usuario_id` | Un usuario puede tener muchos controles de actuadores |

---

### 2.6 Tabla: `sensors`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | SERIAL (PK) | Identificador único del sensor |
| greenhouse_id | INTEGER (FK) | Referencia a `greenhouses.id` |
| tipo | VARCHAR(50) | Tipo de sensor (temperatura, humedad, luz, pH, CO2) |
| nombre | VARCHAR(100) | Nombre del sensor |
| unidad | VARCHAR(20) | Unidad de medida |
| ubicacion | VARCHAR(100) | Ubicación dentro del invernadero |
| estado | BOOLEAN | Estado del sensor |

**Relaciones:**

| Tabla Relacionada | Tipo de Relación | Campo FK | Cardinalidad |
|-------------------|------------------|----------|--------------|
| `greenhouses` | N:1 | `greenhouse_id` → `greenhouses.id` | Muchos sensores pertenecen a un invernadero |
| `sensor_readings` | 1:N | `sensor_readings.sensor_id` | Un sensor puede tener muchas lecturas |
| `alerts` | 1:N | `alerts.sensor_id` | Un sensor puede generar muchas alertas |

---

### 2.7 Tabla: `sensor_readings`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | SERIAL (PK) | Identificador único de la lectura |
| sensor_id | INTEGER (FK) | Referencia a `sensors.id` |
| valor | NUMERIC(10,4) | Valor de la lectura |
| timestamp | TIMESTAMP | Momento de la lectura |
| estado | BOOLEAN | Estado de la lectura |

**Relaciones:**

| Tabla Relacionada | Tipo de Relación | Campo FK | Cardinalidad |
|-------------------|------------------|----------|--------------|
| `sensors` | N:1 | `sensor_id` → `sensors.id` | Muchas lecturas pertenecen a un sensor |

---

### 2.8 Tabla: `crops`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | SERIAL (PK) | Identificador único del cultivo |
| nombre | VARCHAR(100) | Nombre común del cultivo |
| nombre_cientifico | VARCHAR(150) | Nombre científico |
| temperatura_min | NUMERIC(5,2) | Temperatura mínima |
| temperatura_max | NUMERIC(5,2) | Temperatura máxima |
| humedad_min | NUMERIC(5,2) | Humedad mínima |
| humedad_max | NUMERIC(5,2) | Humedad máxima |
| ph_min | NUMERIC(4,2) | pH mínimo del suelo |
| ph_max | NUMERIC(4,2) | pH máximo del suelo |
| ciclo_dias | INTEGER | Días del ciclo de cultivo |
| descripcion | TEXT | Descripción del cultivo |
| estado | BOOLEAN | Estado del cultivo |

**Relaciones:**

| Tabla Relacionada | Tipo de Relación | Campo FK | Cardinalidad |
|-------------------|------------------|----------|--------------|
| `crop_batches` | 1:N | `crop_batches.crop_id` | Un cultivo puede tener muchos lotes |

---

### 2.9 Tabla: `crop_batches`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | SERIAL (PK) | Identificador único del lote |
| crop_id | INTEGER (FK) | Referencia a `crops.id` |
| greenhouse_id | INTEGER (FK) | Referencia a `greenhouses.id` |
| fecha_siembra | DATE | Fecha de siembra |
| fecha_cosecha_estimada | DATE | Fecha estimada de cosecha |
| fecha_cosecha_real | DATE | Fecha real de cosecha |
| cantidad_plantas | INTEGER | Cantidad de plantas |
| estado_cultivo | VARCHAR(30) | Estado del cultivo (creciendo, cosechado, etc.) |
| notas | TEXT | Notas adicionales |
| estado | BOOLEAN | Estado del lote |

**Relaciones:**

| Tabla Relacionada | Tipo de Relación | Campo FK | Cardinalidad |
|-------------------|------------------|----------|--------------|
| `crops` | N:1 | `crop_id` → `crops.id` | Muchos lotes pueden pertenecer a un cultivo |
| `greenhouses` | N:1 | `greenhouse_id` → `greenhouses.id` | Muchos lotes pueden estar en un invernadero |

---

### 2.10 Tabla: `alerts`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | SERIAL (PK) | Identificador único de la alerta |
| greenhouse_id | INTEGER (FK) | Referencia a `greenhouses.id` |
| sensor_id | INTEGER (FK) | Referencia a `sensors.id` |
| tipo | VARCHAR(30) | Tipo de alerta |
| mensaje | TEXT | Mensaje de la alerta |
| valor_actual | NUMERIC(10,4) | Valor que provocó la alerta |
| umbral | NUMERIC(10,4) | Umbral configurado |
| prioridad | VARCHAR(15) | Prioridad (alta, media, baja) |
| estado_alerta | VARCHAR(20) | Estado (activa, resuelta) |
| resuelta_en | TIMESTAMP | Momento de resolución |
| estado | BOOLEAN | Estado general |

**Relaciones:**

| Tabla Relacionada | Tipo de Relación | Campo FK | Cardinalidad |
|-------------------|------------------|----------|--------------|
| `greenhouses` | N:1 | `greenhouse_id` → `greenhouses.id` | Muchas alertas pueden pertenecer a un invernadero |
| `sensors` | N:1 | `sensor_id` → `sensors.id` | Muchas alertas pueden pertenecer a un sensor |

---

### 2.11 Tabla: `irrigation_zones`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | SERIAL (PK) | Identificador único de la zona |
| greenhouse_id | INTEGER (FK) | Referencia a `greenhouses.id` |
| nombre | VARCHAR(100) | Nombre de la zona |
| capacidad_litros_min | NUMERIC(10,2) | Capacidad mínima de litros |
| capacidad_litros_max | NUMERIC(10,2) | Capacidad máxima de litros |
| tipo | VARCHAR(30) | Tipo de riego (gotas, aspersión) |
| estado | BOOLEAN | Estado de la zona |

**Relaciones:**

| Tabla Relacionada | Tipo de Relación | Campo FK | Cardinalidad |
|-------------------|------------------|----------|--------------|
| `greenhouses` | N:1 | `greenhouse_id` → `greenhouses.id` | Muchas zonas de riego pueden pertenecer a un invernadero |
| `irrigation_logs` | 1:N | `irrigation_logs.zone_id` | Una zona puede tener muchos registros de riego |

---

### 2.12 Tabla: `irrigation_logs`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | SERIAL (PK) | Identificador único del registro |
| zone_id | INTEGER (FK) | Referencia a `irrigation_zones.id` |
| duracion_minutos | INTEGER | Duración del riego en minutos |
| cantidad_agua_litros | NUMERIC(10,2) | Cantidad de agua utilizada |
| modo | VARCHAR(20) | Modo de riego (automático, manual) |
| resultado | VARCHAR(20) | Resultado del riego |
| notes | TEXT | Notas adicionales |
| estado | BOOLEAN | Estado del registro |

**Relaciones:**

| Tabla Relacionada | Tipo de Relación | Campo FK | Cardinalidad |
|-------------------|------------------|----------|--------------|
| `irrigation_zones` | N:1 | `zone_id` → `irrigation_zones.id` | Muchos registros de riego pertenecen a una zona |

---

### 2.13 Tabla: `actuators`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | SERIAL (PK) | Identificador único del actuador |
| greenhouse_id | INTEGER (FK) | Referencia a `greenhouses.id` |
| tipo | VARCHAR(50) | Tipo de actuador (ventana, ventilador, bomba, luz) |
| nombre | VARCHAR(100) | Nombre del actuador |
| ubicacion | VARCHAR(100) | Ubicación dentro del invernadero |
| estado_actuador | VARCHAR(20) | Estado (activo, inactivo) |
| estado | BOOLEAN | Estado general |

**Relaciones:**

| Tabla Relacionada | Tipo de Relación | Campo FK | Cardinalidad |
|-------------------|------------------|----------|--------------|
| `greenhouses` | N:1 | `greenhouse_id` → `greenhouses.id` | Muchos actuadores pueden pertenecer a un invernadero |
| `actuator_controls` | 1:N | `actuator_controls.actuator_id` | Un actuador puede tener muchos controles |

---

### 2.14 Tabla: `actuator_controls`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | SERIAL (PK) | Identificador único del control |
| actuator_id | INTEGER (FK) | Referencia a `actuators.id` |
| usuario_id | INTEGER (FK) | Referencia a `usuario.id` |
| accion | VARCHAR(30) | Acción realizada |
| valor_ajuste | VARCHAR(50) | Valor del ajuste |
| resultado | VARCHAR(20) | Resultado del control |
| estado | BOOLEAN | Estado del control |

**Relaciones:**

| Tabla Relacionada | Tipo de Relación | Campo FK | Cardinalidad |
|-------------------|------------------|----------|--------------|
| `actuators` | N:1 | `actuator_id` → `actuators.id` | Muchos controles pueden pertenecer a un actuador |
| `usuario` | N:1 | `usuario_id` → `usuario.id` | Muchos controles pueden ser realizados por un usuario |

---

### 2.15 Tabla: `greenhouse_settings`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | SERIAL (PK) | Identificador único |
| greenhouse_id | INTEGER (FK) | Referencia a `greenhouses.id` |
| temp_min | NUMERIC(5,2) | Temperatura mínima |
| temp_max | NUMERIC(5,2) | Temperatura máxima |
| humedad_min | NUMERIC(5,2) | Humedad mínima |
| humedad_max | NUMERIC(5,2) | Humedad máxima |
| luz_min | NUMERIC(10,2) | Luz mínima |
| ph_min | NUMERIC(4,2) | pH mínimo |
| ph_max | NUMERIC(4,2) | pH máximo |
| intervalo_lectura_minutos | INTEGER | Intervalo de lectura |
| estado | BOOLEAN | Estado |

**Relaciones:**

| Tabla Relacionada | Tipo de Relación | Campo FK | Cardinalidad |
|-------------------|------------------|----------|--------------|
| `greenhouses` | N:1 (1:1) | `greenhouse_id` → `greenhouses.id` | Una configuración pertenece a un invernadero |

**Nota:** Relación 1:1 con `greenhouses` (UNIQUE constraint)

---

### 2.16 Tabla: `sensores_externos`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | SERIAL (PK) | Identificador único del sensor externo |
| tipo | VARCHAR(100) | Tipo de sensor |
| valor_actual | NUMERIC(10,2) | Valor actual |
| ubicacion | VARCHAR(255) | Ubicación |
| estado | BOOLEAN | Estado |

**Relaciones:**

| Tabla Relacionada | Tipo de Relación | Campo FK | Cardinalidad |
|-------------------|------------------|----------|--------------|
| `lecturas_externas` | 1:N | `lecturas_externas.sensor_id` | Un sensor externo puede tener muchas lecturas |

---

### 2.17 Tabla: `lecturas_externas`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | SERIAL (PK) | Identificador único de la lectura |
| sensor_id | INTEGER (FK) | Referencia a `sensores_externos.id` |
| valor | NUMERIC(10,2) | Valor de la lectura |
| timestamp | TIMESTAMP | Momento de la lectura |
| estado | BOOLEAN | Estado de la lectura |

**Relaciones:**

| Tabla Relacionada | Tipo de Relación | Campo FK | Cardinalidad |
|-------------------|------------------|----------|--------------|
| `sensores_externos` | N:1 | `sensor_id` → `sensores_externos.id` | Muchas lecturas externas pertenecen a un sensor |

---

### 2.18 Tabla: `alertas_externas`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | SERIAL (PK) | Identificador único de la alerta |
| mensaje | TEXT | Mensaje de la alerta |
| prioridad | VARCHAR(20) | Prioridad (alta, media, baja) |
| estado | BOOLEAN | Estado de la alerta |
| creado | TIMESTAMP | Fecha de creación |

**Relaciones:** Esta tabla no tiene relaciones con otras tablas del sistema.

---

## 3. RESUMEN DE RELACIONES (1:N y N:1)

| Tabla Padre | Tabla Hijo | Campo FK | Tipo |
|-------------|------------|----------|------|
| `rol` | `usuario` | `usuario.rol_id` | 1:N |
| `rol` | `moduloxrol` | `moduloxrol.rol_id` | 1:N |
| `modulo` | `moduloxrol` | `moduloxrol.modulo_id` | 1:N |
| `greenhouses` | `sensors` | `sensors.greenhouse_id` | 1:N |
| `greenhouses` | `crop_batches` | `crop_batches.greenhouse_id` | 1:N |
| `greenhouses` | `alerts` | `alerts.greenhouse_id` | 1:N |
| `greenhouses` | `irrigation_zones` | `irrigation_zones.greenhouse_id` | 1:N |
| `greenhouses` | `actuators` | `actuators.greenhouse_id` | 1:N |
| `greenhouses` | `greenhouse_settings` | `greenhouse_settings.greenhouse_id` | 1:1 |
| `usuario` | `actuator_controls` | `actuator_controls.usuario_id` | 1:N |
| `sensors` | `sensor_readings` | `sensor_readings.sensor_id` | 1:N |
| `sensors` | `alerts` | `alerts.sensor_id` | 1:N |
| `crops` | `crop_batches` | `crop_batches.crop_id` | 1:N |
| `irrigation_zones` | `irrigation_logs` | `irrigation_logs.zone_id` | 1:N |
| `actuators` | `actuator_controls` | `actuator_controls.actuator_id` | 1:N |
| `sensores_externos` | `lecturas_externas` | `lecturas_externas.sensor_id` | 1:N |

---

## 4. RESUMEN DE RELACIONES MUCHOS A MUCHOS (N:M)

| Tabla A | Tabla B | Tabla Intermedia |
|---------|---------|-----------------|
| `rol` | `modulo` | `moduloxrol` |

La tabla `moduloxrol` representa una relación N:M entre roles y módulos, donde se definen permisos específicos (ver, crear, editar, eliminar) para cada combinación rol-módulo.

---

## 5. ESQUEMA DE RELACIONES COMPLETO

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           SISTEMA DE GESTIÓN DE INVERNADEROS                    │
│                              Grow A Garden API - Base de Datos                  │
└─────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────┐         ┌────────────────┐         ┌──────────┐
    │   rol    │───1:N──│    moduloxrol   │───N:1───│  modulo  │
    └──────────┘         └────────────────┘         └──────────┘
          │
          │ 1:N
          ▼
    ┌──────────┐
    │ usuario  │───1:N───┌───────────────────┐
    └──────────┘         │ actuator_controls │
          │              └───────────────────┘
          │                      ▲
          │                      │ N:1
          │              ┌──────────────┐
          │              │  actuators   │
          │              └──────────────┘
          │                     │
          │ N:1                 │
          ▼                     ▼
    ┌────────────┐      ┌────────────────┐
    │ greenhouses│───1:N─│ greenhouse_    │
    │            │      │ settings       │
    └────────────┘      └────────────────┘
          │
          │ 1:N
          │
    ┌─────┴──────────────────────────────────────────┐
    │                                                  │
    ▼                                                  ▼
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│ sensors  │  │crop_     │  │  alerts  │  │irrigation│  │ actuators│
│          │  │batches   │  │          │  │_zones    │  │          │
└──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘
    │              │              │              │
    │ 1:N          │ 1:N         │ 1:N          │ 1:N
    ▼              │              │              ▼
┌──────────┐      │              │      ┌──────────────┐
│sensor_   │      │              │      │irrigation_   │
│readings  │      │              │      │logs          │
└──────────┘      │              │      └──────────────┘
                  │              │
                  ▼              ▼
            ┌──────────┐  ┌──────────┐
            │  crops   │  │  sensors │
            └──────────┘  └──────────┘

    ┌─────────────────┐         ┌────────────────────┐
    │ sensores_externos│───1:N──│lecturas_externas  │
    └─────────────────┘         └────────────────────┘

    ┌─────────────────┐
    │ alertas_externas │  (sin relaciones)
    └─────────────────┘
```

---

*Documento generado para presentación impresa - Grow A Garden API*
*Autores: Esteban Gomez Jimenez, Victor Daniel Amaranto Garizabalo, Jose Muñoz Perez*
