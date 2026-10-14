-- =====================================================
-- POSTGRESQL - Grow A Garden API (FastAPI)
-- Para usar en bddiagram.io
-- 18 TABLAS
-- =====================================================

-- =====================================================
-- TABLA 1: rol
-- =====================================================
CREATE TABLE rol (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion VARCHAR(200),
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- TABLA 2: modulo
-- =====================================================
CREATE TABLE modulo (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion VARCHAR(200),
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- TABLA 3: moduloxrol (Relación N:M rol - modulo)
-- =====================================================
CREATE TABLE moduloxrol (
    id SERIAL PRIMARY KEY,
    rol_id INTEGER NOT NULL REFERENCES rol(id) ON DELETE CASCADE,
    modulo_id INTEGER NOT NULL REFERENCES modulo(id) ON DELETE CASCADE,
    puede_ver BOOLEAN DEFAULT FALSE,
    puede_crear BOOLEAN DEFAULT FALSE,
    puede_editar BOOLEAN DEFAULT FALSE,
    puede_eliminar BOOLEAN DEFAULT FALSE,
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(rol_id, modulo_id)
);

-- =====================================================
-- TABLA 4: greenhouses
-- =====================================================
CREATE TABLE greenhouses (
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
-- TABLA 5: usuario
-- =====================================================
CREATE TABLE usuario (
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
-- TABLA 6: sensors
-- =====================================================
CREATE TABLE sensors (
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
-- TABLA 7: sensor_readings
-- =====================================================
CREATE TABLE sensor_readings (
    id SERIAL PRIMARY KEY,
    sensor_id INTEGER NOT NULL REFERENCES sensors(id) ON DELETE CASCADE,
    valor NUMERIC(10,4) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- TABLA 8: crops
-- =====================================================
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
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- TABLA 9: crop_batches
-- =====================================================
CREATE TABLE crop_batches (
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
-- TABLA 10: alerts
-- =====================================================
CREATE TABLE alerts (
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
-- TABLA 11: irrigation_zones
-- =====================================================
CREATE TABLE irrigation_zones (
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
-- TABLA 12: irrigation_logs
-- =====================================================
CREATE TABLE irrigation_logs (
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
-- TABLA 13: actuators
-- =====================================================
CREATE TABLE actuators (
    id SERIAL PRIMARY KEY,
    greenhouse_id INTEGER NOT NULL REFERENCES greenhouses(id) ON DELETE CASCADE,
    tipo VARCHAR(50) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    ubicacion VARCHAR(100),
    estado_actuador VARCHAR(20) DEFAULT 'inactivo',
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- TABLA 14: actuator_controls
-- =====================================================
CREATE TABLE actuator_controls (
    id SERIAL PRIMARY KEY,
    actuator_id INTEGER NOT NULL REFERENCES actuators(id) ON DELETE CASCADE,
    usuario_id INTEGER REFERENCES usuario(id) ON DELETE SET NULL,
    accion VARCHAR(30) NOT NULL,
    valor_ajuste VARCHAR(50),
    resultado VARCHAR(20) DEFAULT 'exitoso',
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- TABLA 15: greenhouse_settings
-- =====================================================
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
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- TABLA 16: sensores_externos
-- =====================================================
CREATE TABLE sensores_externos (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(100) NOT NULL,
    valor_actual NUMERIC(10,2),
    ubicacion VARCHAR(255),
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- TABLA 17: lecturas_externas
-- =====================================================
CREATE TABLE lecturas_externas (
    id SERIAL PRIMARY KEY,
    sensor_id INTEGER REFERENCES sensores_externos(id) ON DELETE CASCADE,
    valor NUMERIC(10,2) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- TABLA 18: alertas_externas (SIN RELACIONES)
-- =====================================================
CREATE TABLE alertas_externas (
    id SERIAL PRIMARY KEY,
    mensaje TEXT NOT NULL,
    prioridad VARCHAR(20) DEFAULT 'media',
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- ÍNDICES
-- =====================================================
CREATE INDEX idx_sensor_readings_sensor_id ON sensor_readings(sensor_id);
CREATE INDEX idx_sensor_readings_timestamp ON sensor_readings(timestamp DESC);
CREATE INDEX idx_alerts_greenhouse_id ON alerts(greenhouse_id);
CREATE INDEX idx_alerts_estado ON alerts(estado_alerta);
CREATE INDEX idx_crop_batches_estado ON crop_batches(estado_cultivo);
CREATE INDEX idx_irrigation_logs_zone_id ON irrigation_logs(zone_id);
CREATE INDEX idx_actuator_controls_actuator_id ON actuator_controls(actuator_id);
CREATE INDEX idx_usuario_username ON usuario(username);
CREATE INDEX idx_usuario_email ON usuario(email);
