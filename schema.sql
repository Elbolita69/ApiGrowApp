-- ==========================================================================
-- ApiGrowApp - Esquema de base de datos
-- Motor: PostgreSQL 15 (destino Neon)
-- Descripcion: greenhouse inteligente con invernaderos, sensores, riego,
--             actuadores, alertas, catalogo de cultivos y control de acceso
--              por roles y modulos (matriz moduloxrol).
--
-- Reglas del contrato:
--   * 16 tablas, todas con auditoria: creado, actualizado y estado.
--   * 'estado' es el BORRADO LOGICO: TRUE = registro activo, FALSE = eliminado.
--     El borrado fisico esta prohibido; la API solo hace UPDATE ... SET estado = FALSE.
--   * Trigger set_actualizado() BEFORE UPDATE sobre las 16 tablas.
--   * El archivo es idempotente: se puede ejecutar varias veces sobre la misma base.
--
-- Semillas incluidas: 10 roles, 16 modulos, matriz de permisos, 21 usuarios
--   (hash bcrypt reales, coste 12) y datos operativos de 20 invernaderos,
--   20 cultivos, 20 sensores, 60 lecturas, 20 lotes, 40 alertas, 20 zonas de
--   riego, 20 riegos, 20 actuadores, 20 controles, 20 configuraciones y
--   10 estudiantes.
-- ==========================================================================


-- ==========================================================================
-- SECCION 0. LIMPIEZA IDEMPOTENTE (DROP TABLE ... CASCADE)
-- ==========================================================================
-- Las tablas se eliminan en orden de dependencia inverso (primero las que
-- dependen de otras). Se usa CASCADE para no dejar dependencias huerfanas.
-- Nunca se elimina la base de datos ni el esquema: solo las tablas del modelo.
DROP TABLE IF EXISTS actuator_controls CASCADE;
DROP TABLE IF EXISTS actuators CASCADE;
DROP TABLE IF EXISTS irrigation_logs CASCADE;
DROP TABLE IF EXISTS irrigation_zones CASCADE;
DROP TABLE IF EXISTS alerts CASCADE;
DROP TABLE IF EXISTS sensor_readings CASCADE;
DROP TABLE IF EXISTS sensors CASCADE;
DROP TABLE IF EXISTS crop_batches CASCADE;
DROP TABLE IF EXISTS crops CASCADE;
DROP TABLE IF EXISTS greenhouse_settings CASCADE;
DROP TABLE IF EXISTS estudiantes CASCADE;
DROP TABLE IF EXISTS usuario CASCADE;
DROP TABLE IF EXISTS moduloxrol CASCADE;
DROP TABLE IF EXISTS modulo CASCADE;
DROP TABLE IF EXISTS rol CASCADE;
DROP TABLE IF EXISTS greenhouses CASCADE;

-- La funcion del trigger se recrea en la seccion 2 (queda sin dependencias
-- porque las tablas anteriores fueron eliminadas con sus triggers).
DROP FUNCTION IF EXISTS set_actualizado();


-- ==========================================================================
-- SECCION 1. DDL - ESTRUCTURA DE TABLAS (16 tablas)
-- ==========================================================================
-- Convencion de auditoria, presente en las 16 tablas:
--   estado      BOOLEAN    -> borrado logico (TRUE activo / FALSE eliminado)
--   creado      TIMESTAMP  -> fecha de creacion del registro
--   actualizado TIMESTAMP  -> fecha de la ultima actualizacion (trigger)
-- Las llaves foraneas usan ON DELETE CASCADE, salvo usuario.rol_id (SET NULL)
-- y moduloxrol (SET NULL / RESTRICT), porque son relaciones de configuracion
-- que no deben destruir datos historicos.

-- Tabla: rol
CREATE TABLE rol (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion VARCHAR(200),
    -- Auditoria: estado = borrado logico (TRUE activo / FALSE eliminado)
    estado BOOLEAN NOT NULL DEFAULT TRUE,
    creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: modulo
CREATE TABLE modulo (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion VARCHAR(200),
    -- Auditoria: estado = borrado logico (TRUE activo / FALSE eliminado)
    estado BOOLEAN NOT NULL DEFAULT TRUE,
    creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: moduloxrol
CREATE TABLE moduloxrol (
    id SERIAL PRIMARY KEY,
    rol_id INTEGER REFERENCES rol(id) ON DELETE SET NULL,
    modulo_id INTEGER NOT NULL REFERENCES modulo(id) ON DELETE RESTRICT,
    puede_ver BOOLEAN NOT NULL DEFAULT FALSE,
    puede_crear BOOLEAN NOT NULL DEFAULT FALSE,
    puede_editar BOOLEAN NOT NULL DEFAULT FALSE,
    puede_eliminar BOOLEAN NOT NULL DEFAULT FALSE,
    -- Auditoria: estado = borrado logico (TRUE activo / FALSE eliminado)
    estado BOOLEAN NOT NULL DEFAULT TRUE,
    creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_moduloxrol_rol_modulo UNIQUE (rol_id, modulo_id)
);

-- Tabla: usuario
CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    rol_id INTEGER REFERENCES rol(id) ON DELETE SET NULL,
    -- Auditoria: estado = borrado logico (TRUE activo / FALSE eliminado)
    estado BOOLEAN NOT NULL DEFAULT TRUE,
    creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: greenhouses
CREATE TABLE greenhouses (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    ubicacion VARCHAR(200),
    area_metros_cuadrados NUMERIC(10,2),
    capacidad_maxima INTEGER,
    -- Auditoria: estado = borrado logico (TRUE activo / FALSE eliminado)
    estado BOOLEAN NOT NULL DEFAULT TRUE,
    creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: sensors
CREATE TABLE sensors (
    id SERIAL PRIMARY KEY,
    greenhouse_id INTEGER NOT NULL REFERENCES greenhouses(id) ON DELETE CASCADE,
    tipo VARCHAR(50) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    unidad VARCHAR(20) NOT NULL,
    ubicacion VARCHAR(100),
    -- Auditoria: estado = borrado logico (TRUE activo / FALSE eliminado)
    estado BOOLEAN NOT NULL DEFAULT TRUE,
    creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: sensor_readings
CREATE TABLE sensor_readings (
    id SERIAL PRIMARY KEY,
    sensor_id INTEGER NOT NULL REFERENCES sensors(id) ON DELETE CASCADE,
    valor NUMERIC(10,4) NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -- Auditoria: estado = borrado logico (TRUE activo / FALSE eliminado)
    estado BOOLEAN NOT NULL DEFAULT TRUE,
    creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: crops
CREATE TABLE crops (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    nombre_cientifico VARCHAR(150),
    temperatura_min NUMERIC(5,2),
    temperatura_max NUMERIC(5,2),
    humedad_min NUMERIC(5,2),
    humedad_max NUMERIC(5,2),
    ph_min NUMERIC(4,2),
    ph_max NUMERIC(4,2),
    ciclo_dias INTEGER,
    descripcion TEXT,
    -- Auditoria: estado = borrado logico (TRUE activo / FALSE eliminado)
    estado BOOLEAN NOT NULL DEFAULT TRUE,
    creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: crop_batches
CREATE TABLE crop_batches (
    id SERIAL PRIMARY KEY,
    crop_id INTEGER REFERENCES crops(id) ON DELETE CASCADE,
    greenhouse_id INTEGER NOT NULL REFERENCES greenhouses(id) ON DELETE CASCADE,
    fecha_siembra DATE NOT NULL,
    fecha_cosecha_estimada DATE,
    fecha_cosecha_real DATE,
    cantidad_plantas INTEGER,
    estado_cultivo VARCHAR(30) DEFAULT 'creciendo',
    notas TEXT,
    -- Auditoria: estado = borrado logico (TRUE activo / FALSE eliminado)
    estado BOOLEAN NOT NULL DEFAULT TRUE,
    creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: alerts
CREATE TABLE alerts (
    id SERIAL PRIMARY KEY,
    greenhouse_id INTEGER NOT NULL REFERENCES greenhouses(id) ON DELETE CASCADE,
    sensor_id INTEGER REFERENCES sensors(id) ON DELETE CASCADE,
    tipo VARCHAR(30) NOT NULL,
    mensaje TEXT NOT NULL,
    valor_actual NUMERIC(10,4),
    umbral NUMERIC(10,4),
    prioridad VARCHAR(15) DEFAULT 'media',
    estado_alerta VARCHAR(20) DEFAULT 'activa',
    resuelta_en TIMESTAMP,
    -- Auditoria: estado = borrado logico (TRUE activo / FALSE eliminado)
    estado BOOLEAN NOT NULL DEFAULT TRUE,
    creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: irrigation_zones
CREATE TABLE irrigation_zones (
    id SERIAL PRIMARY KEY,
    greenhouse_id INTEGER NOT NULL REFERENCES greenhouses(id) ON DELETE CASCADE,
    nombre VARCHAR(100) NOT NULL,
    capacidad_litros_min NUMERIC(10,2),
    capacidad_litros_max NUMERIC(10,2),
    tipo VARCHAR(30) DEFAULT 'gotas',
    -- Auditoria: estado = borrado logico (TRUE activo / FALSE eliminado)
    estado BOOLEAN NOT NULL DEFAULT TRUE,
    creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: irrigation_logs
CREATE TABLE irrigation_logs (
    id SERIAL PRIMARY KEY,
    zone_id INTEGER NOT NULL REFERENCES irrigation_zones(id) ON DELETE CASCADE,
    duracion_minutos INTEGER NOT NULL,
    cantidad_agua_litros NUMERIC(10,2),
    modo VARCHAR(20) DEFAULT 'automatico',
    resultado VARCHAR(20) DEFAULT 'exitoso',
    notas TEXT,
    -- Auditoria: estado = borrado logico (TRUE activo / FALSE eliminado)
    estado BOOLEAN NOT NULL DEFAULT TRUE,
    creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: actuators
CREATE TABLE actuators (
    id SERIAL PRIMARY KEY,
    greenhouse_id INTEGER NOT NULL REFERENCES greenhouses(id) ON DELETE CASCADE,
    tipo VARCHAR(50) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    ubicacion VARCHAR(100),
    estado_actuador VARCHAR(20) DEFAULT 'inactivo',
    -- Auditoria: estado = borrado logico (TRUE activo / FALSE eliminado)
    estado BOOLEAN NOT NULL DEFAULT TRUE,
    creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: actuator_controls
CREATE TABLE actuator_controls (
    id SERIAL PRIMARY KEY,
    actuator_id INTEGER NOT NULL REFERENCES actuators(id) ON DELETE CASCADE,
    usuario_id INTEGER REFERENCES usuario(id) ON DELETE CASCADE,
    accion VARCHAR(30) NOT NULL,
    valor_ajuste VARCHAR(50),
    resultado VARCHAR(20) DEFAULT 'exitoso',
    -- Auditoria: estado = borrado logico (TRUE activo / FALSE eliminado)
    estado BOOLEAN NOT NULL DEFAULT TRUE,
    creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: greenhouse_settings
CREATE TABLE greenhouse_settings (
    id SERIAL PRIMARY KEY,
    greenhouse_id INTEGER NOT NULL REFERENCES greenhouses(id) ON DELETE CASCADE UNIQUE,
    temp_min NUMERIC(5,2) DEFAULT 15.00,
    temp_max NUMERIC(5,2) DEFAULT 30.00,
    humedad_min NUMERIC(5,2) DEFAULT 40.00,
    humedad_max NUMERIC(5,2) DEFAULT 80.00,
    luz_min NUMERIC(10,2) DEFAULT 100.00,
    ph_min NUMERIC(4,2) DEFAULT 5.50,
    ph_max NUMERIC(4,2) DEFAULT 7.00,
    intervalo_lectura_minutos INTEGER DEFAULT 15,
    -- Auditoria: estado = borrado logico (TRUE activo / FALSE eliminado)
    estado BOOLEAN NOT NULL DEFAULT TRUE,
    creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: estudiantes
CREATE TABLE estudiantes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    grado VARCHAR(20) NOT NULL,
    promedio NUMERIC(4,2),
    -- Auditoria: estado = borrado logico (TRUE activo / FALSE eliminado)
    estado BOOLEAN NOT NULL DEFAULT TRUE,
    creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- ==========================================================================
-- SECCION 2. FUNCION Y TRIGGERS DE ACTUALIZACION
-- ==========================================================================
-- set_actualizado() se dispara BEFORE UPDATE en las 16 tablas y mantiene
-- actualizado = CURRENT_TIMESTAMP sin que la API tenga que enviarlo.
CREATE OR REPLACE FUNCTION set_actualizado() RETURNS TRIGGER AS $$
BEGIN
    NEW.actualizado = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_rol_actualizado BEFORE UPDATE ON rol FOR EACH ROW EXECUTE FUNCTION set_actualizado();
CREATE TRIGGER trg_modulo_actualizado BEFORE UPDATE ON modulo FOR EACH ROW EXECUTE FUNCTION set_actualizado();
CREATE TRIGGER trg_moduloxrol_actualizado BEFORE UPDATE ON moduloxrol FOR EACH ROW EXECUTE FUNCTION set_actualizado();
CREATE TRIGGER trg_usuario_actualizado BEFORE UPDATE ON usuario FOR EACH ROW EXECUTE FUNCTION set_actualizado();
CREATE TRIGGER trg_greenhouses_actualizado BEFORE UPDATE ON greenhouses FOR EACH ROW EXECUTE FUNCTION set_actualizado();
CREATE TRIGGER trg_sensors_actualizado BEFORE UPDATE ON sensors FOR EACH ROW EXECUTE FUNCTION set_actualizado();
CREATE TRIGGER trg_sensor_readings_actualizado BEFORE UPDATE ON sensor_readings FOR EACH ROW EXECUTE FUNCTION set_actualizado();
CREATE TRIGGER trg_crops_actualizado BEFORE UPDATE ON crops FOR EACH ROW EXECUTE FUNCTION set_actualizado();
CREATE TRIGGER trg_crop_batches_actualizado BEFORE UPDATE ON crop_batches FOR EACH ROW EXECUTE FUNCTION set_actualizado();
CREATE TRIGGER trg_alerts_actualizado BEFORE UPDATE ON alerts FOR EACH ROW EXECUTE FUNCTION set_actualizado();
CREATE TRIGGER trg_irrigation_zones_actualizado BEFORE UPDATE ON irrigation_zones FOR EACH ROW EXECUTE FUNCTION set_actualizado();
CREATE TRIGGER trg_irrigation_logs_actualizado BEFORE UPDATE ON irrigation_logs FOR EACH ROW EXECUTE FUNCTION set_actualizado();
CREATE TRIGGER trg_actuators_actualizado BEFORE UPDATE ON actuators FOR EACH ROW EXECUTE FUNCTION set_actualizado();
CREATE TRIGGER trg_actuator_controls_actualizado BEFORE UPDATE ON actuator_controls FOR EACH ROW EXECUTE FUNCTION set_actualizado();
CREATE TRIGGER trg_greenhouse_settings_actualizado BEFORE UPDATE ON greenhouse_settings FOR EACH ROW EXECUTE FUNCTION set_actualizado();
CREATE TRIGGER trg_estudiantes_actualizado BEFORE UPDATE ON estudiantes FOR EACH ROW EXECUTE FUNCTION set_actualizado();


-- ==========================================================================
-- SECCION 3. INDICES
-- ==========================================================================
-- 3.1 Llaves foraneas consultadas por la API
CREATE INDEX idx_moduloxrol_rol_id ON moduloxrol(rol_id);
CREATE INDEX idx_moduloxrol_modulo_id ON moduloxrol(modulo_id);
CREATE INDEX idx_usuario_rol_id ON usuario(rol_id);
CREATE INDEX idx_sensors_greenhouse_id ON sensors(greenhouse_id);
CREATE INDEX idx_sensor_readings_sensor_id ON sensor_readings(sensor_id);
CREATE INDEX idx_crop_batches_crop_id ON crop_batches(crop_id);
CREATE INDEX idx_crop_batches_greenhouse_id ON crop_batches(greenhouse_id);
CREATE INDEX idx_alerts_greenhouse_id ON alerts(greenhouse_id);
CREATE INDEX idx_alerts_sensor_id ON alerts(sensor_id);
CREATE INDEX idx_irrigation_zones_greenhouse_id ON irrigation_zones(greenhouse_id);
CREATE INDEX idx_irrigation_logs_zone_id ON irrigation_logs(zone_id);
CREATE INDEX idx_actuators_greenhouse_id ON actuators(greenhouse_id);
CREATE INDEX idx_actuator_controls_actuator_id ON actuator_controls(actuator_id);
CREATE INDEX idx_actuator_controls_usuario_id ON actuator_controls(usuario_id);

-- 3.2 Indices adicionales de consulta frecuente
CREATE INDEX idx_usuario_username ON usuario(username);
CREATE INDEX idx_usuario_email ON usuario(email);
CREATE INDEX idx_sensor_readings_timestamp ON sensor_readings(timestamp DESC);
CREATE INDEX idx_alerts_estado_alerta ON alerts(estado_alerta);
CREATE INDEX idx_crop_batches_estado_cultivo ON crop_batches(estado_cultivo);
CREATE INDEX idx_irrigation_logs_fecha ON irrigation_logs(creado DESC);

-- 3.3 Indices de auditoria: borrado logico (estado) y orden por fecha de creacion
-- (Nota: greenhouse_settings.greenhouse_id ya esta indexado por la constraint UNIQUE)
CREATE INDEX idx_rol_estado ON rol(estado);
CREATE INDEX idx_modulo_estado ON modulo(estado);
CREATE INDEX idx_moduloxrol_estado ON moduloxrol(estado);
CREATE INDEX idx_usuario_estado ON usuario(estado);
CREATE INDEX idx_greenhouses_estado ON greenhouses(estado);
CREATE INDEX idx_sensors_estado ON sensors(estado);
CREATE INDEX idx_sensor_readings_estado ON sensor_readings(estado);
CREATE INDEX idx_crops_estado ON crops(estado);
CREATE INDEX idx_crop_batches_estado ON crop_batches(estado);
CREATE INDEX idx_alerts_estado ON alerts(estado);
CREATE INDEX idx_irrigation_zones_estado ON irrigation_zones(estado);
CREATE INDEX idx_irrigation_logs_estado ON irrigation_logs(estado);
CREATE INDEX idx_actuators_estado ON actuators(estado);
CREATE INDEX idx_actuator_controls_estado ON actuator_controls(estado);
CREATE INDEX idx_greenhouse_settings_estado ON greenhouse_settings(estado);
CREATE INDEX idx_estudiantes_estado ON estudiantes(estado);
CREATE INDEX idx_rol_creado ON rol(creado);
CREATE INDEX idx_modulo_creado ON modulo(creado);
CREATE INDEX idx_moduloxrol_creado ON moduloxrol(creado);
CREATE INDEX idx_usuario_creado ON usuario(creado);
CREATE INDEX idx_greenhouses_creado ON greenhouses(creado);
CREATE INDEX idx_sensors_creado ON sensors(creado);
CREATE INDEX idx_sensor_readings_creado ON sensor_readings(creado);
CREATE INDEX idx_crops_creado ON crops(creado);
CREATE INDEX idx_crop_batches_creado ON crop_batches(creado);
CREATE INDEX idx_alerts_creado ON alerts(creado);
CREATE INDEX idx_irrigation_zones_creado ON irrigation_zones(creado);
CREATE INDEX idx_irrigation_logs_creado ON irrigation_logs(creado);
CREATE INDEX idx_actuators_creado ON actuators(creado);
CREATE INDEX idx_actuator_controls_creado ON actuator_controls(creado);
CREATE INDEX idx_greenhouse_settings_creado ON greenhouse_settings(creado);
CREATE INDEX idx_estudiantes_creado ON estudiantes(creado);


-- ==========================================================================
-- SECCION 4. SEMILLAS (datos iniciales)
-- ==========================================================================

-- 4.1 Roles (10) - el orden define los rol_id 1..10
INSERT INTO rol (nombre, descripcion) VALUES
    ('administrador', 'Administra el sistema completo: usuarios, roles, permisos y modulos'),
    ('supervisor', 'Supervisa la operacion diaria de los invernaderos y del equipo de campo'),
    ('agronomo', 'Gestiona cultivos, lotes, parametros agronomicos y alertas'),
    ('regador', 'Programa y ejecuta el riego, las zonas de riego y los actuadores'),
    ('tecnico', 'Mantenimiento tecnico de sensores, lecturas y actuadores'),
    ('auxiliar_riego', 'Apoya las rutinas de riego y la revision de las zonas'),
    ('planificador', 'Planifica siembras, lotes y ciclos de cultivo'),
    ('calidad', 'Revisa la calidad del cultivo y el cumplimiento de los rangos'),
    ('mantenimiento', 'Mantenimiento preventivo de actuadores, sensores e infraestructura'),
    ('lector', 'Solo consulta la informacion de operacion y de cultivos');

-- 4.2 Modulos (16) - el orden define los modulo_id 1..16
INSERT INTO modulo (nombre, descripcion) VALUES
    ('greenhouses', 'Gestion de los invernaderos (nombre, ubicacion y capacidad)'),
    ('sensors', 'Catalogo de sensores instalados por invernadero'),
    ('sensor_readings', 'Historico de lecturas de los sensores'),
    ('crops', 'Catalogo de cultivos y sus rangos agroclimaticos'),
    ('crop_batches', 'Lotes de cultivo sembrados en cada invernadero'),
    ('alerts', 'Alertas generadas por sensores y parametros ambientales'),
    ('irrigation_zones', 'Zonas de riego configuradas por invernadero'),
    ('irrigation_logs', 'Historial de las ejecuciones de riego'),
    ('actuators', 'Actuadores: ventanas, ventiladores, bombas y luces'),
    ('actuator_controls', 'Ordenes de control enviadas a los actuadores'),
    ('greenhouse_settings', 'Parametros ambientales configurados por invernadero'),
    ('usuario', 'Usuarios del sistema y su rol asignado'),
    ('estudiantes', 'Registro de estudiantes vinculados al proyecto'),
    ('sensores_externos', 'Sensores de terceros integrados al sistema'),
    ('lecturas_externas', 'Lecturas provenientes de sensores externos'),
    ('alertas_externas', 'Alertas provenientes de fuentes externas');

-- 4.3 Matriz de permisos rol x modulo (86 filas)
--     Un rol puede ver lo que otro rol registra: los modulos de negocio
--     (crops, crop_batches, alerts, sensor_readings, irrigation_logs) son
--     visibles para varios roles para que el proceso se pueda cerrar.
INSERT INTO moduloxrol (rol_id, modulo_id, puede_ver, puede_crear, puede_editar, puede_eliminar) VALUES
    (1, 1, TRUE, TRUE, TRUE, TRUE),
    (1, 2, TRUE, TRUE, TRUE, TRUE),
    (1, 3, TRUE, TRUE, TRUE, TRUE),
    (1, 4, TRUE, TRUE, TRUE, TRUE),
    (1, 5, TRUE, TRUE, TRUE, TRUE),
    (1, 6, TRUE, TRUE, TRUE, TRUE),
    (1, 7, TRUE, TRUE, TRUE, TRUE),
    (1, 8, TRUE, TRUE, TRUE, TRUE),
    (1, 9, TRUE, TRUE, TRUE, TRUE),
    (1, 10, TRUE, TRUE, TRUE, TRUE),
    (1, 11, TRUE, TRUE, TRUE, TRUE),
    (1, 12, TRUE, TRUE, TRUE, TRUE),
    (1, 13, TRUE, TRUE, TRUE, TRUE),
    (1, 14, TRUE, TRUE, TRUE, TRUE),
    (1, 15, TRUE, TRUE, TRUE, TRUE),
    (1, 16, TRUE, TRUE, TRUE, TRUE),
    (2, 1, TRUE, TRUE, TRUE, TRUE),
    (2, 2, TRUE, TRUE, TRUE, TRUE),
    (2, 3, TRUE, TRUE, TRUE, TRUE),
    (2, 4, TRUE, TRUE, TRUE, TRUE),
    (2, 5, TRUE, TRUE, TRUE, TRUE),
    (2, 6, TRUE, TRUE, TRUE, TRUE),
    (2, 7, TRUE, TRUE, TRUE, TRUE),
    (2, 8, TRUE, TRUE, TRUE, TRUE),
    (2, 9, TRUE, TRUE, TRUE, TRUE),
    (2, 10, TRUE, TRUE, TRUE, TRUE),
    (2, 11, TRUE, TRUE, TRUE, TRUE),
    (2, 12, TRUE, TRUE, TRUE, FALSE),
    (2, 13, TRUE, TRUE, TRUE, TRUE),
    (2, 14, TRUE, TRUE, TRUE, TRUE),
    (2, 15, TRUE, TRUE, TRUE, TRUE),
    (2, 16, TRUE, TRUE, TRUE, TRUE),
    (3, 1, TRUE, FALSE, FALSE, FALSE),
    (3, 2, TRUE, FALSE, FALSE, FALSE),
    (3, 3, TRUE, FALSE, FALSE, FALSE),
    (3, 4, TRUE, TRUE, TRUE, TRUE),
    (3, 5, TRUE, TRUE, TRUE, TRUE),
    (3, 6, TRUE, TRUE, TRUE, TRUE),
    (3, 11, TRUE, TRUE, TRUE, TRUE),
    (3, 13, TRUE, TRUE, TRUE, FALSE),
    (3, 15, TRUE, TRUE, TRUE, FALSE),
    (3, 16, TRUE, TRUE, TRUE, FALSE),
    (4, 1, TRUE, FALSE, FALSE, FALSE),
    (4, 2, TRUE, FALSE, FALSE, FALSE),
    (4, 3, TRUE, FALSE, FALSE, FALSE),
    (4, 6, TRUE, FALSE, TRUE, FALSE),
    (4, 7, TRUE, TRUE, TRUE, TRUE),
    (4, 8, TRUE, TRUE, TRUE, FALSE),
    (4, 9, TRUE, TRUE, TRUE, FALSE),
    (4, 10, TRUE, TRUE, TRUE, FALSE),
    (5, 1, TRUE, FALSE, FALSE, FALSE),
    (5, 2, TRUE, TRUE, TRUE, TRUE),
    (5, 3, TRUE, TRUE, TRUE, FALSE),
    (5, 6, TRUE, FALSE, FALSE, FALSE),
    (5, 9, TRUE, TRUE, TRUE, TRUE),
    (5, 10, TRUE, TRUE, TRUE, FALSE),
    (5, 11, TRUE, FALSE, FALSE, FALSE),
    (6, 1, TRUE, FALSE, FALSE, FALSE),
    (6, 3, TRUE, FALSE, FALSE, FALSE),
    (6, 7, TRUE, TRUE, FALSE, FALSE),
    (6, 8, TRUE, TRUE, FALSE, FALSE),
    (7, 1, TRUE, FALSE, FALSE, FALSE),
    (7, 4, TRUE, FALSE, TRUE, FALSE),
    (7, 5, TRUE, TRUE, FALSE, FALSE),
    (7, 6, TRUE, FALSE, FALSE, FALSE),
    (7, 11, TRUE, FALSE, FALSE, FALSE),
    (7, 13, TRUE, FALSE, FALSE, FALSE),
    (8, 1, TRUE, FALSE, FALSE, FALSE),
    (8, 3, TRUE, FALSE, FALSE, FALSE),
    (8, 4, TRUE, FALSE, FALSE, FALSE),
    (8, 5, TRUE, FALSE, FALSE, FALSE),
    (8, 6, TRUE, FALSE, TRUE, FALSE),
    (8, 13, TRUE, FALSE, FALSE, FALSE),
    (9, 1, TRUE, FALSE, FALSE, FALSE),
    (9, 2, TRUE, FALSE, TRUE, FALSE),
    (9, 9, TRUE, FALSE, TRUE, FALSE),
    (9, 10, TRUE, TRUE, FALSE, FALSE),
    (9, 11, TRUE, FALSE, FALSE, FALSE),
    (10, 1, TRUE, FALSE, FALSE, FALSE),
    (10, 2, TRUE, FALSE, FALSE, FALSE),
    (10, 3, TRUE, FALSE, FALSE, FALSE),
    (10, 4, TRUE, FALSE, FALSE, FALSE),
    (10, 5, TRUE, FALSE, FALSE, FALSE),
    (10, 6, TRUE, FALSE, FALSE, FALSE),
    (10, 8, TRUE, FALSE, FALSE, FALSE),
    (10, 13, TRUE, FALSE, FALSE, FALSE);

-- 4.4 Usuarios (21)
--     Contrasenas (bcrypt, coste 12, bcrypt.hashpw(pw, bcrypt.gensalt())):
--       admin = Admin123*          | supervisor = Supervisor123*
--       agronomo = Agronomo123*    | regador = Regador123*
--       tecnico = Tecnico123*      | lector = Lector123*
--       auxiliar_riego = AuxiliarRiego123* | planificador = Planificador123*
--       calidad = Calidad123*      | mantenimiento = Mantenimiento123*
INSERT INTO usuario (username, email, password_hash, nombre, rol_id) VALUES
    ('admin', 'admin@growapp.co', '$2b$12$HT2V4XTV6AqhcMQFu2HkzOR7Yp1piiJFusGan/7iJ9P9T5J84pd7e', 'Carlos Andres Ramirez', 1),
    ('supervisor1', 'supervisor1@growapp.co', '$2b$12$lJUuBnybDXM1WFYyqqe5QOALMMne.MW5LnmcOnxE6X3E8djuP1yvO', 'Juan Pablo Rojas', 2),
    ('supervisor2', 'supervisor2@growapp.co', '$2b$12$lJUuBnybDXM1WFYyqqe5QOALMMne.MW5LnmcOnxE6X3E8djuP1yvO', 'Maria Fernanda Gomez', 2),
    ('agronomo1', 'agronomo1@growapp.co', '$2b$12$zi/KdQODFsxaE5jnhlkry.0Fl4xJPp.8aeooNiq.f3DhKdO3w99UO', 'Sandra Milena Torres', 3),
    ('agronomo2', 'agronomo2@growapp.co', '$2b$12$zi/KdQODFsxaE5jnhlkry.0Fl4xJPp.8aeooNiq.f3DhKdO3w99UO', 'Ricardo Alonso Beltran', 3),
    ('agronomo3', 'agronomo3@growapp.co', '$2b$12$zi/KdQODFsxaE5jnhlkry.0Fl4xJPp.8aeooNiq.f3DhKdO3w99UO', 'Claudia Patricia Mendoza', 3),
    ('agronomo4', 'agronomo4@growapp.co', '$2b$12$zi/KdQODFsxaE5jnhlkry.0Fl4xJPp.8aeooNiq.f3DhKdO3w99UO', 'Hector Fabian Rincon', 3),
    ('regador1', 'regador1@growapp.co', '$2b$12$aGkwHLBGL0WwUWWSdw2oMOzGFXtSFsizTSZkmeXnS2td096dg27im', 'Luis Alberto Castro', 4),
    ('regador2', 'regador2@growapp.co', '$2b$12$aGkwHLBGL0WwUWWSdw2oMOzGFXtSFsizTSZkmeXnS2td096dg27im', 'Diana Carolina Pardo', 4),
    ('regador3', 'regador3@growapp.co', '$2b$12$aGkwHLBGL0WwUWWSdw2oMOzGFXtSFsizTSZkmeXnS2td096dg27im', 'Andres Felipe Mejia', 4),
    ('regador4', 'regador4@growapp.co', '$2b$12$aGkwHLBGL0WwUWWSdw2oMOzGFXtSFsizTSZkmeXnS2td096dg27im', 'Laura Sofia Herrera', 4),
    ('tecnico1', 'tecnico1@growapp.co', '$2b$12$m19.yV0vYoHkMVP5zXNu/e6Spb8rPT6Au1j/3x4LyQIPN6UQl19PW', 'Jorge Enrique Vargas', 5),
    ('tecnico2', 'tecnico2@growapp.co', '$2b$12$m19.yV0vYoHkMVP5zXNu/e6Spb8rPT6Au1j/3x4LyQIPN6UQl19PW', 'Paola Andrea Cruz', 5),
    ('tecnico3', 'tecnico3@growapp.co', '$2b$12$m19.yV0vYoHkMVP5zXNu/e6Spb8rPT6Au1j/3x4LyQIPN6UQl19PW', 'Camilo Ernesto Ortiz', 5),
    ('lector1', 'lector1@growapp.co', '$2b$12$.OaWjylzJf0rVfR6SbZjpuihi/4ShgiBgcK/0lKQsYWBUHe7iD0cS', 'Natalia Rocio Salazar', 10),
    ('lector2', 'lector2@growapp.co', '$2b$12$.OaWjylzJf0rVfR6SbZjpuihi/4ShgiBgcK/0lKQsYWBUHe7iD0cS', 'Oscar Mauricio Duarte', 10),
    ('lector3', 'lector3@growapp.co', '$2b$12$.OaWjylzJf0rVfR6SbZjpuihi/4ShgiBgcK/0lKQsYWBUHe7iD0cS', 'Angela Maria Silva', 10),
    ('auxiliar_riego1', 'auxiliar_riego1@growapp.co', '$2b$12$KU5MfBrY9tD615rWyOXQmuhwvCYXlNdR71b99Q7AbYPuVphj6ulOy', 'Daniel Esteban Acosta', 6),
    ('planificador1', 'planificador1@growapp.co', '$2b$12$PVWPt1qtT8O9Gh/11MU1jebl1HZ6mw9VE4MQ9hb/lb1jQ.dd/8x3i', 'Monica Lucia Forero', 7),
    ('calidad1', 'calidad1@growapp.co', '$2b$12$EyZTQUSBOLvFGipS3.Jcy.nJjldC4COM4kdzahLzKbB7Im7b1G9Vq', 'Viviana Alejandra Leon', 8),
    ('mantenimiento1', 'mantenimiento1@growapp.co', '$2b$12$DOsFjELxosEJ8DVdCpmOoOIKVrrnE1nxmZqt2VFp3xsK1lLmgXto2', 'Jorge Dario Buitrago', 9);

-- 4.5 Invernaderos (20)
INSERT INTO greenhouses (nombre, ubicacion, area_metros_cuadrados, capacidad_maxima) VALUES
    ('Invernadero Tomate Chonto Cajica', 'Cajica, Cundinamarca', 1200.0, 6000),
    ('Invernadero Lechugas Chia', 'Chia, Cundinamarca', 800.0, 9000),
    ('Invernadero Fresas Sopo', 'Sopo, Cundinamarca', 650.0, 7500),
    ('Invernadero Pimenton Facatativa', 'Facatativa, Cundinamarca', 900.0, 4500),
    ('Invernadero Pepino Tenjo', 'Tenjo, Cundinamarca', 700.0, 3500),
    ('Invernadero Flores Zipaquira', 'Zipaquira, Cundinamarca', 1500.0, 12000),
    ('Invernadero Aromaticas La Ceja', 'La Ceja, Antioquia', 500.0, 5000),
    ('Invernadero Tomate Rionegro', 'Rionegro, Antioquia', 1100.0, 5500),
    ('Invernadero Mora Marinilla', 'Marinilla, Antioquia', 600.0, 2400),
    ('Invernadero Hortalizas El Penol', 'El Penol, Antioquia', 750.0, 6000),
    ('Invernadero Tomate Palmira', 'Palmira, Valle del Cauca', 1300.0, 6500),
    ('Invernadero Pimenton Tulua', 'Tulua, Valle del Cauca', 950.0, 4750),
    ('Invernadero Lechuga Buga', 'Buga, Valle del Cauca', 700.0, 8400),
    ('Invernadero Cebolla Cartago', 'Cartago, Valle del Cauca', 850.0, 12000),
    ('Invernadero Tomate Ibague', 'Ibague, Tolima', 1000.0, 5000),
    ('Invernadero Pepino Espinal', 'Espinal, Tolima', 780.0, 3900),
    ('Invernadero Fresas Tunja', 'Tunja, Boyaca', 560.0, 6720),
    ('Invernadero Habichuela Duitama', 'Duitama, Boyaca', 640.0, 7680),
    ('Invernadero Tomate Sogamoso', 'Sogamoso, Boyaca', 900.0, 4500),
    ('Invernadero Aji Villavicencio', 'Villavicencio, Meta', 720.0, 3600);

-- 4.6 Cultivos (20)
INSERT INTO crops (nombre, nombre_cientifico, temperatura_min, temperatura_max, humedad_min, humedad_max, ph_min, ph_max, ciclo_dias, descripcion) VALUES
    ('Tomate chonto', 'Solanum lycopersicum', 18.0, 27.0, 60.0, 80.0, 5.5, 6.8, 110, 'Cultivo principal de los invernadero de clima templado en Cundinamarca'),
    ('Lechuga batavia', 'Lactuca sativa', 10.0, 20.0, 70.0, 90.0, 5.8, 6.6, 55, 'Hoja de ciclo corto sembrada en Tunja y Buga'),
    ('Fresa', 'Fragaria x ananassa', 15.0, 25.0, 65.0, 80.0, 5.5, 6.5, 120, 'Fruto de alto valor comercial para mercado de Sopo y Tunja'),
    ('Pimenton', 'Capsicum annuum', 18.0, 28.0, 50.0, 70.0, 5.8, 6.8, 95, 'Fruto de clima calido manejado en Facatativa y Tulua'),
    ('Pepino cohombro', 'Cucumis sativus', 20.0, 30.0, 75.0, 90.0, 5.5, 6.8, 65, 'Cucurbitacea de alta demanda de humedad en Tenjo y Espinal'),
    ('Cebolla larga', 'Allium fistulosum', 12.0, 24.0, 60.0, 80.0, 6.0, 7.0, 100, 'Bulbo de ciclo largo para comercializacion en Zipaquira'),
    ('Mora de Castilla', 'Rubus glaucus', 14.0, 22.0, 70.0, 85.0, 5.5, 6.5, 240, 'Cultivo perenne de 240 dias manejado en La Ceja'),
    ('Habichuela', 'Phaseolus vulgaris', 16.0, 27.0, 60.0, 75.0, 6.0, 7.0, 70, 'Leguminosa de ciclo corto sembrada en Rionegro y Duitama'),
    ('Aji', 'Capsicum baccatum', 20.0, 30.0, 55.0, 75.0, 6.0, 7.0, 100, 'Picante andino de porte medio para Villavicencio'),
    ('Cilantro', 'Coriandrum sativum', 12.0, 22.0, 60.0, 75.0, 6.2, 6.8, 45, 'Hierba aromatica de ciclo muy corto para rotations rapidas'),
    ('Perejil', 'Petroselinum crispum', 12.0, 22.0, 60.0, 75.0, 6.0, 7.0, 70, 'Hierba perenne de hoja abierta y baja exigencia hidrica'),
    ('Albahaca', 'Ocimum basilicum', 18.0, 28.0, 60.0, 75.0, 6.0, 7.0, 60, 'Aromatica de alto valor parailah para ventana caliente'),
    ('Espinaca', 'Spinacia oleracea', 8.0, 20.0, 65.0, 85.0, 6.0, 7.5, 50, 'Hoja resistente al frio sembrada en Buga'),
    ('Acelga', 'Beta vulgaris var. cicla', 10.0, 24.0, 65.0, 80.0, 6.0, 7.5, 60, 'Hoja de tallo coloreado para multicultivo en Cartago'),
    ('Zanahoria', 'Daucus carota', 12.0, 24.0, 60.0, 80.0, 6.0, 6.8, 100, 'Raiz de suelo profundo sembrada en Ibague'),
    ('Rabano', 'Raphanus sativus', 10.0, 22.0, 65.0, 80.0, 6.0, 7.0, 30, 'Raiz de ciclo rapido usada en rotaciones cortas'),
    ('Brocoli', 'Brassica oleracea var. italica', 12.0, 22.0, 65.0, 85.0, 6.0, 7.0, 90, 'Brassica de cabeza compacta para Tunja'),
    ('Coliflor', 'Brassica oleracea var. botrytis', 12.0, 22.0, 65.0, 85.0, 6.0, 7.0, 100, 'Brassica de ciclo mas largo sembrada en Duitama'),
    ('Calabacin', 'Cucurbita pepo', 18.0, 28.0, 60.0, 75.0, 6.0, 7.0, 55, 'Cucurbitacea de fruto immature para Sogamoso'),
    ('Apio', 'Apium graveolens', 12.0, 22.0, 70.0, 85.0, 6.0, 7.0, 110, 'Umbelifera de alta humedad sembrada en Villavicencio');

-- 4.7 Sensores (20)
INSERT INTO sensors (greenhouse_id, tipo, nombre, unidad, ubicacion) VALUES
    (1, 'temperatura', 'Sensor Temperatura 01', 'C', 'Zona norte'),
    (2, 'humedad', 'Sensor Humedad relativa 02', '%', 'Zona sur'),
    (3, 'ph', 'Sensor pH del suelo 03', 'pH', 'Centro'),
    (4, 'luz', 'Sensor Luminosidad 04', 'lux', 'Entrada'),
    (5, 'co2', 'Sensor Dioxido de carbono 05', 'ppm', 'Techo'),
    (6, 'temperatura', 'Sensor Temperatura 06', 'C', 'Zona norte'),
    (7, 'humedad', 'Sensor Humedad relativa 07', '%', 'Zona sur'),
    (8, 'ph', 'Sensor pH del suelo 08', 'pH', 'Centro'),
    (9, 'luz', 'Sensor Luminosidad 09', 'lux', 'Entrada'),
    (10, 'co2', 'Sensor Dioxido de carbono 10', 'ppm', 'Techo'),
    (11, 'temperatura', 'Sensor Temperatura 11', 'C', 'Zona norte'),
    (12, 'humedad', 'Sensor Humedad relativa 12', '%', 'Zona sur'),
    (13, 'ph', 'Sensor pH del suelo 13', 'pH', 'Centro'),
    (14, 'luz', 'Sensor Luminosidad 14', 'lux', 'Entrada'),
    (15, 'co2', 'Sensor Dioxido de carbono 15', 'ppm', 'Techo'),
    (16, 'temperatura', 'Sensor Temperatura 16', 'C', 'Zona norte'),
    (17, 'humedad', 'Sensor Humedad relativa 17', '%', 'Zona sur'),
    (18, 'ph', 'Sensor pH del suelo 18', 'pH', 'Centro'),
    (19, 'luz', 'Sensor Luminosidad 19', 'lux', 'Entrada'),
    (20, 'co2', 'Sensor Dioxido de carbono 20', 'ppm', 'Techo');

-- 4.8 Lecturas de sensores (60)
INSERT INTO sensor_readings (sensor_id, valor, timestamp) VALUES
    (1, 19.19, '2026-10-20 06:00:00'),
    (1, 23.03, '2026-10-25 13:00:00'),
    (1, 24.1, '2026-10-28 06:00:00'),
    (2, 70.35, '2026-10-21 09:07:00'),
    (2, 80.8, '2026-10-26 16:07:00'),
    (2, 76.28, '2026-10-29 06:00:00'),
    (3, 5.73, '2026-10-22 12:14:00'),
    (3, 5.89, '2026-10-27 19:14:00'),
    (3, 6.12, '2026-10-30 06:00:00'),
    (4, 22424.74, '2026-10-20 15:21:00'),
    (4, 21357.42, '2026-10-25 08:21:00'),
    (4, 24580.33, '2026-10-31 06:00:00'),
    (5, 791.69, '2026-10-21 18:28:00'),
    (5, 673.91, '2026-10-26 11:28:00'),
    (5, 742.18, '2026-11-01 06:00:00'),
    (6, 25.31, '2026-10-22 07:35:00'),
    (6, 25.68, '2026-10-27 14:35:00'),
    (6, 23.44, '2026-10-28 07:00:00'),
    (7, 77.53, '2026-10-20 10:42:00'),
    (7, 72.6, '2026-10-25 17:42:00'),
    (7, 74.91, '2026-10-29 07:00:00'),
    (8, 5.91, '2026-10-21 13:49:00'),
    (8, 6.4, '2026-10-26 06:49:00'),
    (8, 6.35, '2026-10-30 07:00:00'),
    (9, 10657.68, '2026-10-22 16:56:00'),
    (9, 27602.27, '2026-10-27 09:56:00'),
    (9, 18990.44, '2026-10-31 07:00:00'),
    (10, 624.83, '2026-10-20 19:03:00'),
    (10, 807.38, '2026-10-25 12:03:00'),
    (10, 688.72, '2026-11-01 07:00:00'),
    (11, 24.85, '2026-10-21 08:10:00'),
    (11, 24.79, '2026-10-26 15:10:00'),
    (11, 26.85, '2026-10-28 08:00:00'),
    (12, 61.31, '2026-10-22 11:17:00'),
    (12, 62.55, '2026-10-27 18:17:00'),
    (12, 68.43, '2026-10-29 08:00:00'),
    (13, 6.87, '2026-10-20 14:24:00'),
    (13, 6.81, '2026-10-25 07:24:00'),
    (13, 5.96, '2026-10-30 08:00:00'),
    (14, 27323.26, '2026-10-21 17:31:00'),
    (14, 31991.75, '2026-10-26 10:31:00'),
    (14, 30112.09, '2026-10-31 08:00:00'),
    (15, 656.79, '2026-10-22 06:38:00'),
    (15, 438.16, '2026-10-27 13:38:00'),
    (15, 815.26, '2026-11-01 08:00:00'),
    (16, 21.4, '2026-10-20 09:45:00'),
    (16, 23.57, '2026-10-25 16:45:00'),
    (16, 25.37, '2026-10-28 09:00:00'),
    (17, 63.76, '2026-10-21 12:52:00'),
    (17, 68.72, '2026-10-26 19:52:00'),
    (17, 71.65, '2026-10-29 09:00:00'),
    (18, 6.74, '2026-10-22 15:59:00'),
    (18, 6.52, '2026-10-27 08:59:00'),
    (18, 6.61, '2026-10-30 09:00:00'),
    (19, 21858.16, '2026-10-20 18:06:00'),
    (19, 8593.74, '2026-10-25 11:06:00'),
    (19, 16754.88, '2026-10-31 09:00:00'),
    (20, 755.43, '2026-10-21 07:13:00'),
    (20, 581.77, '2026-10-26 14:13:00'),
    (20, 604.37, '2026-11-01 09:00:00');

-- 4.9 Lotes de cultivo (20)
INSERT INTO crop_batches (crop_id, greenhouse_id, fecha_siembra, fecha_cosecha_estimada, fecha_cosecha_real, cantidad_plantas, estado_cultivo, notas) VALUES
    (1, 1, '2026-06-01', '2026-09-19', NULL, 582, 'creciendo', 'Lote sembrado en Cajica con riego por goteo.'),
    (2, 2, '2026-06-07', '2026-08-01', NULL, 242, 'creciendo', 'Lote sembrado en Chia con riego por goteo.'),
    (3, 3, '2026-06-13', '2026-10-11', NULL, 558, 'floracion', 'Lote sembrado en Sopo con riego por goteo.'),
    (4, 4, '2026-06-19', '2026-09-22', '2026-09-22', 749, 'cosechado', 'Lote sembrado en Facatativa con riego por goteo.'),
    (5, 5, '2026-06-25', '2026-08-29', NULL, 717, 'creciendo', 'Lote sembrado en Tenjo con riego por goteo.'),
    (6, 6, '2026-07-01', '2026-10-09', NULL, 660, 'creciendo', 'Lote sembrado en Zipaquira con riego por goteo.'),
    (7, 7, '2026-07-07', '2027-03-04', NULL, 269, 'creciendo', 'Lote sembrado en La Ceja con riego por goteo.'),
    (8, 8, '2026-07-13', '2026-09-21', NULL, 585, 'floracion', 'Lote sembrado en Rionegro con riego por goteo.'),
    (9, 9, '2026-07-19', '2026-10-27', '2026-10-27', 668, 'cosechado', 'Lote sembrado en Marinilla con riego por goteo.'),
    (10, 10, '2026-07-25', '2026-09-08', NULL, 764, 'creciendo', 'Lote sembrado en El Penol con riego por goteo.'),
    (11, 11, '2026-07-31', '2026-10-09', NULL, 652, 'creciendo', 'Lote sembrado en Palmira con riego por goteo.'),
    (12, 12, '2026-08-06', '2026-10-05', NULL, 557, 'creciendo', 'Lote sembrado en Tulua con riego por goteo.'),
    (13, 13, '2026-08-12', '2026-10-01', NULL, 687, 'floracion', 'Lote sembrado en Buga con riego por goteo.'),
    (14, 14, '2026-08-18', '2026-10-17', '2026-10-17', 414, 'cosechado', 'Lote sembrado en Cartago con riego por goteo.'),
    (15, 15, '2026-08-24', '2026-12-02', NULL, 580, 'creciendo', 'Lote sembrado en Ibague con riego por goteo.'),
    (16, 16, '2026-08-30', '2026-09-29', NULL, 727, 'creciendo', 'Lote sembrado en Espinal con riego por goteo.'),
    (17, 17, '2026-09-05', '2026-12-04', NULL, 640, 'creciendo', 'Lote sembrado en Tunja con riego por goteo.'),
    (18, 18, '2026-09-11', '2026-12-20', NULL, 675, 'floracion', 'Lote sembrado en Duitama con riego por goteo.'),
    (19, 19, '2026-09-17', '2026-11-11', '2026-11-11', 680, 'cosechado', 'Lote sembrado en Sogamoso con riego por goteo.'),
    (20, 20, '2026-09-23', '2027-01-11', NULL, 175, 'creciendo', 'Lote sembrado en Villavicencio con riego por goteo.');

-- 4.10 Alertas (40)
INSERT INTO alerts (greenhouse_id, sensor_id, tipo, mensaje, valor_actual, umbral, prioridad, estado_alerta, resuelta_en) VALUES
    (1, 1, 'temperatura_alta', 'Temperatura por encima del maximo permitido (Cajica)', 32.23, 28.0, 'alta', 'activa', NULL),
    (2, 2, 'humedad_baja', 'Humedad relativa por debajo del minimo (Chia)', 49.3, 55.0, 'media', 'activa', NULL),
    (3, 3, 'ph_fuera_rango', 'pH del suelo fuera del rango optimo (Sopo)', 8.85, 6.9, 'media', 'reconocida', NULL),
    (4, 4, 'co2_alto', 'Concentracion de CO2 elevada (Facatativa)', 1101.89, 900.0, 'baja', 'resuelta', '2026-10-28 10:30:00'),
    (5, 5, 'luz_baja', 'Luminosidad insuficiente para el cultivo (Tenjo)', 5200.57, 8000.0, 'baja', 'activa', NULL),
    (6, 6, 'temperatura_alta', 'Temperatura por encima del maximo permitido (Zipaquira)', 32.51, 28.0, 'alta', 'activa', NULL),
    (7, 7, 'humedad_baja', 'Humedad relativa por debajo del minimo (La Ceja)', 49.15, 55.0, 'media', 'reconocida', NULL),
    (8, 8, 'ph_fuera_rango', 'pH del suelo fuera del rango optimo (Rionegro)', 7.69, 6.9, 'media', 'resuelta', '2026-10-28 10:30:00'),
    (9, 9, 'co2_alto', 'Concentracion de CO2 elevada (Marinilla)', 1099.43, 900.0, 'baja', 'activa', NULL),
    (10, 10, 'luz_baja', 'Luminosidad insuficiente para el cultivo (El Penol)', 5201.65, 8000.0, 'baja', 'activa', NULL),
    (11, 11, 'temperatura_alta', 'Temperatura por encima del maximo permitido (Palmira)', 33.05, 28.0, 'alta', 'reconocida', NULL),
    (12, 12, 'humedad_baja', 'Humedad relativa por debajo del minimo (Tulua)', 47.37, 55.0, 'media', 'resuelta', '2026-10-28 10:30:00'),
    (13, 13, 'ph_fuera_rango', 'pH del suelo fuera del rango optimo (Buga)', 8.5, 6.9, 'media', 'activa', NULL),
    (14, 14, 'co2_alto', 'Concentracion de CO2 elevada (Cartago)', 1101.02, 900.0, 'baja', 'activa', NULL),
    (15, 15, 'luz_baja', 'Luminosidad insuficiente para el cultivo (Ibague)', 5201.14, 8000.0, 'baja', 'reconocida', NULL),
    (16, 16, 'temperatura_alta', 'Temperatura por encima del maximo permitido (Espinal)', 33.38, 28.0, 'alta', 'resuelta', '2026-10-28 10:30:00'),
    (17, 17, 'humedad_baja', 'Humedad relativa por debajo del minimo (Tunja)', 49.94, 55.0, 'media', 'activa', NULL),
    (18, 18, 'ph_fuera_rango', 'pH del suelo fuera del rango optimo (Duitama)', 7.15, 6.9, 'media', 'activa', NULL),
    (19, 19, 'co2_alto', 'Concentracion de CO2 elevada (Sogamoso)', 1100.21, 900.0, 'baja', 'reconocida', NULL),
    (20, 20, 'luz_baja', 'Luminosidad insuficiente para el cultivo (Villavicencio)', 5201.99, 8000.0, 'baja', 'resuelta', '2026-10-28 10:30:00'),
    (1, 1, 'temperatura_baja', 'Caida nocturna de temperatura bajo el minimo (Cajica)', 15.9, 18.0, 'alta', 'resuelta', '2026-10-26 07:15:00'),
    (2, 2, 'humedad_alta', 'Humedad relativa por encima del maximo (Chia)', 88.4, 85.0, 'media', 'resuelta', '2026-10-27 09:40:00'),
    (3, 3, 'ph_acido', 'pH del suelo por debajo del rango optimo (Sopo)', 5.1, 5.5, 'media', 'resuelta', '2026-10-28 08:05:00'),
    (4, 4, 'luz_baja', 'Luminosidad insuficiente por nubosidad (Facatativa)', 7100.2, 8000.0, 'baja', 'resuelta', '2026-10-27 16:20:00'),
    (5, 5, 'co2_bajo', 'Concentracion de CO2 baja por ventilacion (Tenjo)', 372.6, 400.0, 'media', 'resuelta', '2026-10-29 05:55:00'),
    (6, 6, 'temperatura_baja', 'Caida nocturna de temperatura bajo el minimo (Zipaquira)', 16.4, 18.0, 'alta', 'resuelta', '2026-10-27 03:40:00'),
    (7, 7, 'humedad_alta', 'Humedad relativa por encima del maximo (La Ceja)', 87.2, 85.0, 'media', 'resuelta', '2026-10-28 04:50:00'),
    (8, 8, 'ph_acido', 'pH del suelo por debajo del rango optimo (Rionegro)', 5.2, 5.5, 'media', 'resuelta', '2026-10-29 07:10:00'),
    (9, 9, 'luz_baja', 'Luminosidad insuficiente por nubosidad (Marinilla)', 7450.8, 8000.0, 'baja', 'resuelta', '2026-10-30 06:35:00'),
    (10, 10, 'co2_bajo', 'Concentracion de CO2 baja por ventilacion (El Penol)', 385.1, 400.0, 'media', 'resuelta', '2026-10-28 22:05:00'),
    (11, 11, 'temperatura_baja', 'Caida nocturna de temperatura bajo el minimo (Palmira)', 15.6, 18.0, 'alta', 'resuelta', '2026-10-29 04:30:00'),
    (12, 12, 'humedad_alta', 'Humedad relativa por encima del maximo (Tulua)', 86.9, 85.0, 'media', 'resuelta', '2026-10-30 05:45:00'),
    (13, 13, 'ph_acido', 'pH del suelo por debajo del rango optimo (Buga)', 5.3, 5.5, 'media', 'resuelta', '2026-10-31 06:20:00'),
    (14, 14, 'luz_baja', 'Luminosidad insuficiente por nubosidad (Cartago)', 7050.4, 8000.0, 'baja', 'resuelta', '2026-11-01 05:30:00'),
    (15, 15, 'co2_bajo', 'Concentracion de CO2 baja por ventilacion (Ibague)', 378.9, 400.0, 'media', 'resuelta', '2026-10-30 21:15:00'),
    (16, 16, 'temperatura_baja', 'Caida nocturna de temperatura bajo el minimo (Espinal)', 16.9, 18.0, 'alta', 'resuelta', '2026-10-31 03:50:00'),
    (17, 17, 'humedad_alta', 'Humedad relativa por encima del maximo (Tunja)', 86.1, 85.0, 'media', 'resuelta', '2026-11-01 04:25:00'),
    (18, 18, 'ph_acido', 'pH del suelo por debajo del rango optimo (Duitama)', 5.4, 5.5, 'media', 'resuelta', '2026-11-01 07:40:00'),
    (19, 19, 'luz_baja', 'Luminosidad insuficiente por nubosidad (Sogamoso)', 7280.5, 8000.0, 'baja', 'resuelta', '2026-11-01 18:10:00'),
    (20, 20, 'co2_bajo', 'Concentracion de CO2 baja por ventilacion (Villavicencio)', 390.7, 400.0, 'media', 'resuelta', '2026-10-29 23:05:00');

-- 4.11 Zonas de riego (20)
INSERT INTO irrigation_zones (greenhouse_id, nombre, capacidad_litros_min, capacidad_litros_max, tipo) VALUES
    (1, 'Sector A - Tomate chonto', 80.0, 300.0, 'gotas'),
    (2, 'Sector B - Lechuga batavia', 100.0, 360.0, 'aspersion'),
    (3, 'Sector C - Fresa', 120.0, 420.0, 'microaspersion'),
    (4, 'Sector D - Pimenton', 140.0, 480.0, 'gotas'),
    (5, 'Sector A - Pepino cohombro', 160.0, 540.0, 'aspersion'),
    (6, 'Sector B - Cebolla larga', 80.0, 300.0, 'microaspersion'),
    (7, 'Sector C - Mora de Castilla', 100.0, 360.0, 'gotas'),
    (8, 'Sector D - Habichuela', 120.0, 420.0, 'aspersion'),
    (9, 'Sector A - Aji', 140.0, 480.0, 'microaspersion'),
    (10, 'Sector B - Cilantro', 160.0, 540.0, 'gotas'),
    (11, 'Sector C - Perejil', 80.0, 300.0, 'aspersion'),
    (12, 'Sector D - Albahaca', 100.0, 360.0, 'microaspersion'),
    (13, 'Sector A - Espinaca', 120.0, 420.0, 'gotas'),
    (14, 'Sector B - Acelga', 140.0, 480.0, 'aspersion'),
    (15, 'Sector C - Zanahoria', 160.0, 540.0, 'microaspersion'),
    (16, 'Sector D - Rabano', 80.0, 300.0, 'gotas'),
    (17, 'Sector A - Brocoli', 100.0, 360.0, 'aspersion'),
    (18, 'Sector B - Coliflor', 120.0, 420.0, 'microaspersion'),
    (19, 'Sector C - Calabacin', 140.0, 480.0, 'gotas'),
    (20, 'Sector D - Apio', 160.0, 540.0, 'aspersion');

-- 4.12 Historial de riego (20)
INSERT INTO irrigation_logs (zone_id, duracion_minutos, cantidad_agua_litros, modo, resultado, notas) VALUES
    (1, 10, 65.48, 'automatico', 'exitoso', 'Riego programado segun humedad del suelo.'),
    (2, 15, 91.47, 'manual', 'exitoso', 'Riego programado segun humedad del suelo.'),
    (3, 20, 116.98, 'automatico', 'exitoso', 'Riego programado segun humedad del suelo.'),
    (4, 25, 143.05, 'manual', 'parcial', 'Riego programado segun humedad del suelo.'),
    (5, 30, 164.02, 'automatico', 'exitoso', 'Riego programado segun humedad del suelo.'),
    (6, 35, 187.03, 'manual', 'exitoso', 'Riego programado segun humedad del suelo.'),
    (7, 10, 218.32, 'automatico', 'exitoso', 'Riego programado segun humedad del suelo.'),
    (8, 15, 60.09, 'manual', 'parcial', 'Riego programado segun humedad del suelo.'),
    (9, 20, 86.5, 'automatico', 'exitoso', 'Riego programado segun humedad del suelo.'),
    (10, 25, 118.82, 'manual', 'exitoso', 'Riego programado segun humedad del suelo.'),
    (11, 30, 144.61, 'automatico', 'exitoso', 'Riego programado segun humedad del suelo.'),
    (12, 35, 168.04, 'manual', 'parcial', 'Riego programado segun humedad del suelo.'),
    (13, 10, 194.27, 'automatico', 'exitoso', 'Riego programado segun humedad del suelo.'),
    (14, 15, 213.6, 'manual', 'exitoso', 'Riego programado segun humedad del suelo.'),
    (15, 20, 62.0, 'automatico', 'exitoso', 'Riego programado segun humedad del suelo.'),
    (16, 25, 91.93, 'manual', 'parcial', 'Riego programado segun humedad del suelo.'),
    (17, 30, 114.67, 'automatico', 'exitoso', 'Riego programado segun humedad del suelo.'),
    (18, 35, 142.67, 'manual', 'exitoso', 'Riego programado segun humedad del suelo.'),
    (19, 10, 164.97, 'automatico', 'exitoso', 'Riego programado segun humedad del suelo.'),
    (20, 15, 189.34, 'manual', 'parcial', 'Riego programado segun humedad del suelo.');

-- 4.13 Actuadores (20)
INSERT INTO actuators (greenhouse_id, tipo, nombre, ubicacion, estado_actuador) VALUES
    (1, 'ventana', 'Ventana cenital 01', 'Techo', 'inactivo'),
    (2, 'ventilador', 'Ventilador de extraccion 02', 'Pared norte', 'activo'),
    (3, 'bomba_agua', 'Bomba de riego 03', 'Sala tecnica', 'inactivo'),
    (4, 'luz_artificial', 'Lampara de crecimiento 04', 'Centro', 'activo'),
    (5, 'ventana', 'Ventana lateral 05', 'Pared sur', 'inactivo'),
    (6, 'ventana', 'Ventana cenital 06', 'Techo', 'activo'),
    (7, 'ventilador', 'Ventilador de extraccion 07', 'Pared norte', 'inactivo'),
    (8, 'bomba_agua', 'Bomba de riego 08', 'Sala tecnica', 'activo'),
    (9, 'luz_artificial', 'Lampara de crecimiento 09', 'Centro', 'inactivo'),
    (10, 'ventana', 'Ventana lateral 10', 'Pared sur', 'activo'),
    (11, 'ventana', 'Ventana cenital 11', 'Techo', 'inactivo'),
    (12, 'ventilador', 'Ventilador de extraccion 12', 'Pared norte', 'activo'),
    (13, 'bomba_agua', 'Bomba de riego 13', 'Sala tecnica', 'inactivo'),
    (14, 'luz_artificial', 'Lampara de crecimiento 14', 'Centro', 'activo'),
    (15, 'ventana', 'Ventana lateral 15', 'Pared sur', 'inactivo'),
    (16, 'ventana', 'Ventana cenital 16', 'Techo', 'activo'),
    (17, 'ventilador', 'Ventilador de extraccion 17', 'Pared norte', 'inactivo'),
    (18, 'bomba_agua', 'Bomba de riego 18', 'Sala tecnica', 'activo'),
    (19, 'luz_artificial', 'Lampara de crecimiento 19', 'Centro', 'inactivo'),
    (20, 'ventana', 'Ventana lateral 20', 'Pared sur', 'activo');

-- 4.14 Controles de actuadores (20)
INSERT INTO actuator_controls (actuator_id, usuario_id, accion, valor_ajuste, resultado) VALUES
    (1, 2, 'abrir', '100%', 'fallido'),
    (2, 3, 'cerrar', '0%', 'exitoso'),
    (3, 12, 'encender', NULL, 'exitoso'),
    (4, 13, 'apagar', NULL, 'exitoso'),
    (5, 14, 'ajustar', '60%', 'exitoso'),
    (6, 8, 'abrir', '100%', 'exitoso'),
    (7, 9, 'cerrar', '0%', 'exitoso'),
    (8, 10, 'encender', NULL, 'fallido'),
    (9, 11, 'apagar', NULL, 'exitoso'),
    (10, 1, 'ajustar', '60%', 'exitoso'),
    (11, 2, 'abrir', '100%', 'exitoso'),
    (12, 3, 'cerrar', '0%', 'exitoso'),
    (13, 12, 'encender', NULL, 'exitoso'),
    (14, 13, 'apagar', NULL, 'exitoso'),
    (15, 14, 'ajustar', '60%', 'fallido'),
    (16, 8, 'abrir', '100%', 'exitoso'),
    (17, 9, 'cerrar', '0%', 'exitoso'),
    (18, 10, 'encender', NULL, 'exitoso'),
    (19, 11, 'apagar', NULL, 'exitoso'),
    (20, 1, 'ajustar', '60%', 'exitoso');

-- 4.15 Configuracion por invernadero (20)
INSERT INTO greenhouse_settings (greenhouse_id, temp_min, temp_max, humedad_min, humedad_max, luz_min, ph_min, ph_max, intervalo_lectura_minutos) VALUES
    (1, 18.0, 27.0, 60.0, 80.0, 8000.0, 5.5, 6.8, 15),
    (2, 10.0, 20.0, 70.0, 90.0, 9000.0, 5.8, 6.6, 15),
    (3, 15.0, 25.0, 65.0, 80.0, 10000.0, 5.5, 6.5, 15),
    (4, 18.0, 28.0, 50.0, 70.0, 11000.0, 5.8, 6.8, 15),
    (5, 20.0, 30.0, 75.0, 90.0, 8000.0, 5.5, 6.8, 15),
    (6, 12.0, 24.0, 60.0, 80.0, 9000.0, 6.0, 7.0, 15),
    (7, 14.0, 22.0, 70.0, 85.0, 10000.0, 5.5, 6.5, 15),
    (8, 16.0, 27.0, 60.0, 75.0, 11000.0, 6.0, 7.0, 15),
    (9, 20.0, 30.0, 55.0, 75.0, 8000.0, 6.0, 7.0, 15),
    (10, 12.0, 22.0, 60.0, 75.0, 9000.0, 6.2, 6.8, 15),
    (11, 12.0, 22.0, 60.0, 75.0, 10000.0, 6.0, 7.0, 15),
    (12, 18.0, 28.0, 60.0, 75.0, 11000.0, 6.0, 7.0, 15),
    (13, 8.0, 20.0, 65.0, 85.0, 8000.0, 6.0, 7.5, 15),
    (14, 10.0, 24.0, 65.0, 80.0, 9000.0, 6.0, 7.5, 15),
    (15, 12.0, 24.0, 60.0, 80.0, 10000.0, 6.0, 6.8, 15),
    (16, 10.0, 22.0, 65.0, 80.0, 11000.0, 6.0, 7.0, 15),
    (17, 12.0, 22.0, 65.0, 85.0, 8000.0, 6.0, 7.0, 15),
    (18, 12.0, 22.0, 65.0, 85.0, 9000.0, 6.0, 7.0, 15),
    (19, 18.0, 28.0, 60.0, 75.0, 10000.0, 6.0, 7.0, 15),
    (20, 12.0, 22.0, 70.0, 85.0, 11000.0, 6.0, 7.0, 15);

-- 4.16 Estudiantes (10)
INSERT INTO estudiantes (nombre, grado, promedio) VALUES
    ('Ana Sofia Betancur', '10', 4.35),
    ('Juan David Marin', '11', 3.9),
    ('Mariana Lopez Salas', '9', 4.6),
    ('Sebastian Torres Cardona', '10', 3.75),
    ('Isabella Ocampo Pelaez', '8', 4.1),
    ('David Alejandro Quintero', '11', 4.45),
    ('Laura Valentina Rios', '9', 3.6),
    ('Mateo Escobar Zuluaga', '10', 4.2),
    ('Camila Andrea Hoyos', '11', 4.8),
    ('Santiago Villa Sanchez', '8', 3.95);


-- ==========================================================================
-- SECCION 5. COMENTARIOS DE LAS TABLAS
-- ==========================================================================
COMMENT ON TABLE rol IS 'Roles del sistema con los permisos definidos en la matriz moduloxrol';
COMMENT ON TABLE modulo IS 'Modulos de negocio sobre los que se asignan permisos';
COMMENT ON TABLE moduloxrol IS 'Matriz de permisos (ver, crear, editar, eliminar) por rol y modulo';
COMMENT ON TABLE usuario IS 'Usuarios de la aplicacion, con hash bcrypt y rol asociado';
COMMENT ON TABLE greenhouses IS 'Invernaderos de produccion y sus datos de ubicacion y capacidad';
COMMENT ON TABLE sensors IS 'Sensores instalados en cada invernadero';
COMMENT ON TABLE sensor_readings IS 'Serie historica de lecturas de cada sensor';
COMMENT ON TABLE crops IS 'Catalogo de cultivos con sus rangos agroclimaticos';
COMMENT ON TABLE crop_batches IS 'Lotes de cultivo sembrados en cada invernadero';
COMMENT ON TABLE alerts IS 'Alertas ambientales generadas por los sensores y los parametros';
COMMENT ON TABLE irrigation_zones IS 'Zonas de riego configuradas por invernadero';
COMMENT ON TABLE irrigation_logs IS 'Historial de ejecuciones de riego por zona';
COMMENT ON TABLE actuators IS 'Actuadores: ventanas, ventiladores, bombas de riego y luces';
COMMENT ON TABLE actuator_controls IS 'Ordenes de control ejecutadas sobre los actuadores por los usuarios';
COMMENT ON TABLE greenhouse_settings IS 'Parametros ambientales configurados para cada invernadero';
COMMENT ON TABLE estudiantes IS 'Estudiantes vinculados al proyecto educativo de los invernaderos';

-- Fin del esquema ApiGrowApp.
