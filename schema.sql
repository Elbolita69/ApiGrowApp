-- =====================================================
-- INVERNADERO INTELIGENTE - Schema SQL Normalizado
-- Base de datos: PostgreSQL
-- 16 tablas: 12 core + 4 RBAC
-- =====================================================

-- =====================================================
-- RBAC: Roles
-- =====================================================
CREATE TABLE IF NOT EXISTS rol (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion VARCHAR(200),
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- RBAC: Modulos API
-- =====================================================
CREATE TABLE IF NOT EXISTS modulo (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion VARCHAR(200),
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- RBAC: Matriz de Permisos (rol x modulo)
-- =====================================================
CREATE TABLE IF NOT EXISTS moduloxrol (
    id SERIAL PRIMARY KEY,
    rol_id INTEGER NOT NULL REFERENCES rol(id) ON DELETE CASCADE,
    modulo_id INTEGER NOT NULL REFERENCES modulo(id) ON DELETE CASCADE,
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(rol_id, modulo_id)
);

-- =====================================================
-- 1. Tabla: Invernaderos
-- =====================================================
CREATE TABLE IF NOT EXISTS greenhouses (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    ubicacion VARCHAR(200),
    area_metros_cuadrados NUMERIC(10,2),
    capacidad_maxima INTEGER,
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- 2. Tabla: Sensores
-- =====================================================
CREATE TABLE IF NOT EXISTS sensors (
    id SERIAL PRIMARY KEY,
    greenhouse_id INTEGER NOT NULL REFERENCES greenhouses(id) ON DELETE CASCADE,
    tipo VARCHAR(50) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    unidad VARCHAR(20) NOT NULL,
    ubicacion VARCHAR(100),
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- 3. Tabla: Lecturas de Sensores
-- =====================================================
CREATE TABLE IF NOT EXISTS sensor_readings (
    id SERIAL PRIMARY KEY,
    sensor_id INTEGER NOT NULL REFERENCES sensors(id) ON DELETE CASCADE,
    valor NUMERIC(10,4) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- 4. Tabla: Cultivos (catalogo)
-- =====================================================
CREATE TABLE IF NOT EXISTS crops (
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
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- 5. Tabla: Lotes de Cultivos
-- =====================================================
CREATE TABLE IF NOT EXISTS crop_batches (
    id SERIAL PRIMARY KEY,
    crop_id INTEGER REFERENCES crops(id) ON DELETE SET NULL,
    greenhouse_id INTEGER NOT NULL REFERENCES greenhouses(id) ON DELETE CASCADE,
    fecha_siembra DATE NOT NULL,
    fecha_cosecha_estimada DATE,
    fecha_cosecha_real DATE,
    cantidad_plantas INTEGER,
    estado_cultivo VARCHAR(30) DEFAULT 'creciendo',
    notas TEXT,
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- 6. Tabla: Alertas
-- =====================================================
CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    greenhouse_id INTEGER NOT NULL REFERENCES greenhouses(id) ON DELETE CASCADE,
    sensor_id INTEGER REFERENCES sensors(id) ON DELETE SET NULL,
    tipo VARCHAR(30) NOT NULL,
    mensaje TEXT NOT NULL,
    valor_actual NUMERIC(10,4),
    umbral NUMERIC(10,4),
    prioridad VARCHAR(15) DEFAULT 'media',
    estado_alerta VARCHAR(20) DEFAULT 'activa',
    resuelta_en TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- 7. Tabla: Zonas de Riego
-- =====================================================
CREATE TABLE IF NOT EXISTS irrigation_zones (
    id SERIAL PRIMARY KEY,
    greenhouse_id INTEGER NOT NULL REFERENCES greenhouses(id) ON DELETE CASCADE,
    nombre VARCHAR(100) NOT NULL,
    capacidad_litros_min NUMERIC(10,2),
    capacidad_litros_max NUMERIC(10,2),
    tipo VARCHAR(30) DEFAULT 'gotas',
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- 8. Tabla: Historial de Riego
-- =====================================================
CREATE TABLE IF NOT EXISTS irrigation_logs (
    id SERIAL PRIMARY KEY,
    zone_id INTEGER NOT NULL REFERENCES irrigation_zones(id) ON DELETE CASCADE,
    duracion_minutos INTEGER NOT NULL,
    cantidad_agua_litros NUMERIC(10,2),
    modo VARCHAR(20) DEFAULT 'automatico',
    resultado VARCHAR(20) DEFAULT 'exitoso',
    notes TEXT,
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- 9. Tabla: Actuadores
-- =====================================================
CREATE TABLE IF NOT EXISTS actuators (
    id SERIAL PRIMARY KEY,
    greenhouse_id INTEGER NOT NULL REFERENCES greenhouses(id) ON DELETE CASCADE,
    tipo VARCHAR(50) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    ubicacion VARCHAR(100),
    estado_actuador VARCHAR(20) DEFAULT 'inactivo',
    fecha_instalacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- 10. Tabla: Control de Actuadores
-- =====================================================
CREATE TABLE IF NOT EXISTS actuator_controls (
    id SERIAL PRIMARY KEY,
    actuator_id INTEGER NOT NULL REFERENCES actuators(id) ON DELETE CASCADE,
    usuario_id INTEGER NOT NULL,
    accion VARCHAR(30) NOT NULL,
    valor_ajuste VARCHAR(50),
    resultado VARCHAR(20) DEFAULT 'exitoso',
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- 11. Tabla: Configuraciones del Invernadero
-- =====================================================
CREATE TABLE IF NOT EXISTS greenhouse_settings (
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
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- 12. Tabla: Usuarios
-- =====================================================
CREATE TABLE IF NOT EXISTS usuario (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    nombre VARCHAR(100),
    rol_id INTEGER REFERENCES rol(id) ON DELETE SET NULL,
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- Indices para optimizar consultas frecuentes
-- =====================================================
CREATE INDEX IF NOT EXISTS idx_sensor_readings_sensor_id ON sensor_readings(sensor_id);
CREATE INDEX IF NOT EXISTS idx_sensor_readings_timestamp ON sensor_readings(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_alerts_greenhouse_id ON alerts(greenhouse_id);
CREATE INDEX IF NOT EXISTS idx_alerts_estado ON alerts(estado_alerta);
CREATE INDEX IF NOT EXISTS idx_crop_batches_estado ON crop_batches(estado_cultivo);
CREATE INDEX IF NOT EXISTS idx_irrigation_logs_zone_id ON irrigation_logs(zone_id);
CREATE INDEX IF NOT EXISTS idx_actuator_controls_actuator_id ON actuator_controls(actuator_id);
CREATE INDEX IF NOT EXISTS idx_usuario_username ON usuario(username);
CREATE INDEX IF NOT EXISTS idx_usuario_email ON usuario(email);

-- =====================================================
-- Seed Data: RBAC
-- =====================================================

-- Roles
INSERT INTO rol (nombre, descripcion) VALUES
('administrador', 'Administrador del sistema con acceso total'),
('operador', 'Operador de invernaderos con permisos de lectura y escritura'),
('readonly', 'Solo lectura, sin permisos de escritura');

-- Modulos (11 modulos correspondientes a cada tabla/ruta)
INSERT INTO modulo (nombre, descripcion) VALUES
('greenhouses', 'Gestion de invernaderos'),
('sensors', 'Gestion de sensores'),
('sensor_readings', 'Lecturas de sensores'),
('crops', 'Catalogo de cultivos'),
('crop_batches', 'Lotes de cultivos'),
('alerts', 'Alertas del sistema'),
('irrigation_zones', 'Zonas de riego'),
('irrigation_logs', 'Historial de riego'),
('actuators', 'Actuadores'),
('actuator_controls', 'Control de actuadores'),
('greenhouse_settings', 'Configuraciones'),
('usuario', 'Gestion de usuarios');

-- Permisos: Todos los roles tienen acceso a todos los modulos
-- Administrador: acceso total
INSERT INTO moduloxrol (rol_id, modulo_id)
SELECT r.id, m.id FROM rol r, modulo m WHERE r.nombre = 'administrador';

-- Operador: acceso total
INSERT INTO moduloxrol (rol_id, modulo_id)
SELECT r.id, m.id FROM rol r, modulo m WHERE r.nombre = 'operador';

-- Readonly: solo lectura (moduloxrol con estado=FALSE para denotar solo lectura)
-- Para readonly, todos los modulos pero sin permiso de escritura (indicado por rol readonly)
INSERT INTO moduloxrol (rol_id, modulo_id)
SELECT r.id, m.id FROM rol r, modulo m WHERE r.nombre = 'readonly';

-- =====================================================
-- Seed Data: Tablas Core
-- =====================================================

INSERT INTO greenhouses (nombre, ubicacion, area_metros_cuadrados, capacidad_maxima) VALUES
('Invernadero Principal', 'Zona Norte - Sector A', 500.00, 1000),
('Invernadero Secundario', 'Zona Sur - Sector B', 300.00, 500);

INSERT INTO crops (nombre, nombre_cientifico, temperatura_min, temperatura_max, humedad_min, humedad_max, ciclo_dias) VALUES
('Tomate', 'Solanum lycopersicum', 18.00, 27.00, 60.00, 80.00, 90),
('Lechuga', 'Lactuca sativa', 10.00, 20.00, 70.00, 90.00, 45),
('Pepino', 'Cucumis sativus', 20.00, 30.00, 75.00, 90.00, 60),
('Pimiento', 'Capsicum annuum', 18.00, 28.00, 50.00, 70.00, 75),
('Fresas', 'Fragaria × ananassa', 15.00, 25.00, 65.00, 80.00, 120);

INSERT INTO sensors (greenhouse_id, tipo, nombre, unidad, ubicacion) VALUES
(1, 'temperatura', 'Sensor Temp 1', '°C', 'Esquina NW'),
(1, 'temperatura', 'Sensor Temp 2', '°C', 'Esquina SE'),
(1, 'humedad', 'Sensor Humedad 1', '%', 'Centro'),
(1, 'luz', 'Sensor Luz 1', 'lux', 'Techo'),
(1, 'ph', 'Sensor pH 1', 'pH', 'Suelo A1'),
(1, 'co2', 'Sensor CO2 1', 'ppm', 'Centro'),
(2, 'temperatura', 'Sensor Temp 3', '°C', 'Esquina NW'),
(2, 'humedad', 'Sensor Humedad 2', '%', 'Centro');

INSERT INTO irrigation_zones (greenhouse_id, nombre, capacidad_litros_min, capacidad_litros_max, tipo) VALUES
(1, 'Zona A - Tomates', 100.00, 500.00, 'gotas'),
(1, 'Zona B - Lechugas', 50.00, 200.00, 'gotas'),
(2, 'Zona C - General', 150.00, 600.00, 'aspersión');

INSERT INTO actuators (greenhouse_id, tipo, nombre, ubicacion) VALUES
(1, 'ventana', 'Ventana Norte', 'Pared Norte'),
(1, 'ventana', 'Ventana Sur', 'Pared Sur'),
(1, 'ventilador', 'Ventilador Principal', 'Centro'),
(1, 'bomba_agua', 'Bomba Riego Principal', 'Sala Técnica'),
(1, 'luz_artificial', 'Luces Crecimiento', 'Techo'),
(2, 'ventilador', 'Ventilador Secundario', 'Esquina SE');

INSERT INTO greenhouse_settings (greenhouse_id, temp_min, temp_max, humedad_min, humedad_max) VALUES
(1, 18.00, 28.00, 60.00, 80.00),
(2, 15.00, 30.00, 50.00, 85.00);

INSERT INTO usuario (username, email, password_hash, nombre, rol_id) VALUES
('admin', 'admin@greenhouse.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4p', 'Administrador', (SELECT id FROM rol WHERE nombre = 'administrador')),
('operador1', 'operador1@greenhouse.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4p', 'Juan Pérez', (SELECT id FROM rol WHERE nombre = 'operador'));
