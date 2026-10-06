-- =====================================================
-- INVERNADERO INTELIGENTE - Schema SQL
-- Base de datos: PostgreSQL (Neon)
-- =====================================================

-- 1. Tabla: Invernaderos
CREATE TABLE IF NOT EXISTS greenhouses (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    ubicacion VARCHAR(200),
    area_metros_cuadrados NUMERIC(10,2),
    capacidad_maxima INTEGER,
    estado VARCHAR(20) DEFAULT 'activo',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabla: Sensores
CREATE TABLE IF NOT EXISTS sensors (
    id SERIAL PRIMARY KEY,
    greenhouse_id INTEGER REFERENCES greenhouses(id) ON DELETE CASCADE,
    tipo VARCHAR(50) NOT NULL, -- temperatura, humedad, luz, ph, co2
    nombre VARCHAR(100) NOT NULL,
    unidad VARCHAR(20) NOT NULL, -- °C, %, lux, pH, ppm
    ubicacion VARCHAR(100),
    estado VARCHAR(20) DEFAULT 'activo',
    fecha_instalacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Tabla: Lecturas de Sensores
CREATE TABLE IF NOT EXISTS sensor_readings (
    id SERIAL PRIMARY KEY,
    sensor_id INTEGER REFERENCES sensors(id) ON DELETE CASCADE,
    valor NUMERIC(10,4) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Tabla: Cultivos (catálogo)
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
    descripcion TEXT
);

-- 5. Tabla: Lotes de Cultivos
CREATE TABLE IF NOT EXISTS crop_batches (
    id SERIAL PRIMARY KEY,
    crop_id INTEGER REFERENCES crops(id) ON DELETE SET NULL,
    greenhouse_id INTEGER REFERENCES greenhouses(id) ON DELETE CASCADE,
    fecha_siembra DATE NOT NULL,
    fecha_cosecha_estimada DATE,
    fecha_cosecha_real DATE,
    cantidad_plantas INTEGER,
    estado VARCHAR(30) DEFAULT 'creciendo', -- germinando, creciendo, maduro, cosechado
    notas TEXT
);

-- 6. Tabla: Usuarios
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nombre VARCHAR(100),
    rol VARCHAR(20) DEFAULT 'operador', -- administrador, operador, readonly
    estado VARCHAR(20) DEFAULT 'activo',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. Tabla: Alertas
CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    greenhouse_id INTEGER REFERENCES greenhouses(id) ON DELETE CASCADE,
    sensor_id INTEGER REFERENCES sensors(id) ON DELETE SET NULL,
    tipo VARCHAR(30) NOT NULL, -- temperatura_alta, temperatura_baja, humedad_alta, humedad_baja, etc.
    mensaje TEXT NOT NULL,
    valor_actual NUMERIC(10,4),
    umbral NUMERIC(10,4),
    prioridad VARCHAR(15) DEFAULT 'media', -- baja, media, alta, critica
    estado VARCHAR(20) DEFAULT 'activa', -- activa, reconocida, resuelta
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resuelta_en TIMESTAMP
);

-- 8. Tabla: Zonas de Riego
CREATE TABLE IF NOT EXISTS irrigation_zones (
    id SERIAL PRIMARY KEY,
    greenhouse_id INTEGER REFERENCES greenhouses(id) ON DELETE CASCADE,
    nombre VARCHAR(100) NOT NULL,
    capacidadLitros_min NUMERIC(10,2),
    capacidadLitros_max NUMERIC(10,2),
    tipo VARCHAR(30) DEFAULT 'gotas', -- gotes, aspersión, inundación
    estado VARCHAR(20) DEFAULT 'activo'
);

-- 9. Tabla: Historial de Riego
CREATE TABLE IF NOT EXISTS irrigation_logs (
    id SERIAL PRIMARY KEY,
    zone_id INTEGER REFERENCES irrigation_zones(id) ON DELETE CASCADE,
    duracion_minutos INTEGER NOT NULL,
    cantidad_agua_litros NUMERIC(10,2),
    modo VARCHAR(20) DEFAULT 'automatico', -- automatico, manual, programado
    resultado VARCHAR(20) DEFAULT 'exitoso', -- exitoso, fallido, cancelado
    notes TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 10. Tabla: Actuadores
CREATE TABLE IF NOT EXISTS actuators (
    id SERIAL PRIMARY KEY,
    greenhouse_id INTEGER REFERENCES greenhouses(id) ON DELETE CASCADE,
    tipo VARCHAR(50) NOT NULL, -- ventana, ventilador, bomba_agua, luz_artificial, caldera
    nombre VARCHAR(100) NOT NULL,
    ubicacion VARCHAR(100),
    estado VARCHAR(20) DEFAULT 'inactivo', -- activo, inactivo, mantenimiento
    fecha_instalacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 11. Tabla: Control de Actuadores
CREATE TABLE IF NOT EXISTS actuator_controls (
    id SERIAL PRIMARY KEY,
    actuator_id INTEGER REFERENCES actuators(id) ON DELETE CASCADE,
    usuario_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    accion VARCHAR(30) NOT NULL, -- abrir, cerrar, encender, apagar, ajustar
    valor_ajuste VARCHAR(50),
    resultado VARCHAR(20) DEFAULT 'exitoso', -- exitoso, fallido
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 12. Tabla: Configuraciones del Invernadero
CREATE TABLE IF NOT EXISTS greenhouse_settings (
    id SERIAL PRIMARY KEY,
    greenhouse_id INTEGER REFERENCES greenhouses(id) ON DELETE CASCADE UNIQUE,
    temp_min NUMERIC(5,2) DEFAULT 15.00,
    temp_max NUMERIC(5,2) DEFAULT 30.00,
    humedad_min NUMERIC(5,2) DEFAULT 40.00,
    humedad_max NUMERIC(5,2) DEFAULT 80.00,
    luz_min NUMERIC(10,2) DEFAULT 100.00,
    ph_min NUMERIC(4,2) DEFAULT 5.50,
    ph_max NUMERIC(4,2) DEFAULT 7.00,
    intervalo_lectura_minutos INTEGER DEFAULT 15,
    actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- Índices para optimizar consultas frecuentes
-- =====================================================
CREATE INDEX IF NOT EXISTS idx_sensor_readings_sensor_id ON sensor_readings(sensor_id);
CREATE INDEX IF NOT EXISTS idx_sensor_readings_timestamp ON sensor_readings(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_alerts_estado ON alerts(estado);
CREATE INDEX IF NOT EXISTS idx_alerts_greenhouse_id ON alerts(greenhouse_id);
CREATE INDEX IF NOT EXISTS idx_crop_batches_estado ON crop_batches(estado);
CREATE INDEX IF NOT EXISTS idx_irrigation_logs_zone_id ON irrigation_logs(zone_id);
CREATE INDEX IF NOT EXISTS idx_actuator_controls_actuator_id ON actuator_controls(actuator_id);

-- =====================================================
-- Datos de ejemplo (seed data)
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

INSERT INTO irrigation_zones (greenhouse_id, nombre, capacidadLitros_min, capacidadLitros_max, tipo) VALUES
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

INSERT INTO users (username, email, password_hash, nombre, rol) VALUES
('admin', 'admin@greenhouse.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4p', 'Administrador', 'administrador'),
('operador1', 'operador1@greenhouse.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4p', 'Juan Pérez', 'operador');

INSERT INTO greenhouse_settings (greenhouse_id, temp_min, temp_max, humedad_min, humedad_max) VALUES
(1, 18.00, 28.00, 60.00, 80.00),
(2, 15.00, 30.00, 50.00, 85.00);
