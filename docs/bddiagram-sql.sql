-- =====================================================
-- BASE DE DATOS: grow_garden_api
-- Para usar en bddiagram.io
-- =====================================================

-- =====================================================
-- 1. TABLA: rol
-- =====================================================
CREATE TABLE rol (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion VARCHAR(200),
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- =====================================================
-- 2. TABLA: modulo
-- =====================================================
CREATE TABLE modulo (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion VARCHAR(200),
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- =====================================================
-- 3. TABLA: moduloxrol (Relación N:M entre rol y modulo)
-- =====================================================
CREATE TABLE moduloxrol (
    id INT PRIMARY KEY AUTO_INCREMENT,
    rol_id INT NOT NULL,
    modulo_id INT NOT NULL,
    puede_ver BOOLEAN DEFAULT FALSE,
    puede_crear BOOLEAN DEFAULT FALSE,
    puede_editar BOOLEAN DEFAULT FALSE,
    puede_eliminar BOOLEAN DEFAULT FALSE,
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_rol_modulo (rol_id, modulo_id),
    FOREIGN KEY (rol_id) REFERENCES rol(id) ON DELETE CASCADE,
    FOREIGN KEY (modulo_id) REFERENCES modulo(id) ON DELETE CASCADE
);

-- =====================================================
-- 4. TABLA: greenhouses
-- =====================================================
CREATE TABLE greenhouses (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    ubicacion VARCHAR(200),
    area_metros_cuadrados DECIMAL(10,2),
    capacidad_maxima INT,
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- =====================================================
-- 5. TABLA: usuario
-- =====================================================
CREATE TABLE usuario (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    nombre VARCHAR(100),
    rol_id INT,
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (rol_id) REFERENCES rol(id) ON DELETE SET NULL
);

-- =====================================================
-- 6. TABLA: sensors
-- =====================================================
CREATE TABLE sensors (
    id INT PRIMARY KEY AUTO_INCREMENT,
    greenhouse_id INT NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    unidad VARCHAR(20) NOT NULL,
    ubicacion VARCHAR(100),
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (greenhouse_id) REFERENCES greenhouses(id) ON DELETE CASCADE
);

-- =====================================================
-- 7. TABLA: sensor_readings
-- =====================================================
CREATE TABLE sensor_readings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sensor_id INT NOT NULL,
    valor DECIMAL(10,4) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (sensor_id) REFERENCES sensors(id) ON DELETE CASCADE
);

-- =====================================================
-- 8. TABLA: crops
-- =====================================================
CREATE TABLE crops (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    nombre_cientifico VARCHAR(150),
    temperatura_min DECIMAL(5,2),
    temperatura_max DECIMAL(5,2),
    humedad_min DECIMAL(5,2),
    humedad_max DECIMAL(5,2),
    ph_min DECIMAL(4,2),
    ph_max DECIMAL(4,2),
    ciclo_dias INT,
    descripcion TEXT,
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- =====================================================
-- 9. TABLA: crop_batches
-- =====================================================
CREATE TABLE crop_batches (
    id INT PRIMARY KEY AUTO_INCREMENT,
    crop_id INT,
    greenhouse_id INT NOT NULL,
    fecha_siembra DATE NOT NULL,
    fecha_cosecha_estimada DATE,
    fecha_cosecha_real DATE,
    cantidad_plantas INT,
    estado_cultivo VARCHAR(30) DEFAULT 'creciendo',
    notas TEXT,
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (crop_id) REFERENCES crops(id) ON DELETE SET NULL,
    FOREIGN KEY (greenhouse_id) REFERENCES greenhouses(id) ON DELETE CASCADE
);

-- =====================================================
-- 10. TABLA: alerts
-- =====================================================
CREATE TABLE alerts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    greenhouse_id INT NOT NULL,
    sensor_id INT,
    tipo VARCHAR(30) NOT NULL,
    mensaje TEXT NOT NULL,
    valor_actual DECIMAL(10,4),
    umbral DECIMAL(10,4),
    prioridad VARCHAR(15) DEFAULT 'media',
    estado_alerta VARCHAR(20) DEFAULT 'activa',
    resuelta_en TIMESTAMP NULL,
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (greenhouse_id) REFERENCES greenhouses(id) ON DELETE CASCADE,
    FOREIGN KEY (sensor_id) REFERENCES sensors(id) ON DELETE SET NULL
);

-- =====================================================
-- 11. TABLA: irrigation_zones
-- =====================================================
CREATE TABLE irrigation_zones (
    id INT PRIMARY KEY AUTO_INCREMENT,
    greenhouse_id INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    capacidad_litros_min DECIMAL(10,2),
    capacidad_litros_max DECIMAL(10,2),
    tipo VARCHAR(30) DEFAULT 'gotas',
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (greenhouse_id) REFERENCES greenhouses(id) ON DELETE CASCADE
);

-- =====================================================
-- 12. TABLA: irrigation_logs
-- =====================================================
CREATE TABLE irrigation_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    zone_id INT NOT NULL,
    duracion_minutos INT NOT NULL,
    cantidad_agua_litros DECIMAL(10,2),
    modo VARCHAR(20) DEFAULT 'automatico',
    resultado VARCHAR(20) DEFAULT 'exitoso',
    notes TEXT,
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (zone_id) REFERENCES irrigation_zones(id) ON DELETE CASCADE
);

-- =====================================================
-- 13. TABLA: actuators
-- =====================================================
CREATE TABLE actuators (
    id INT PRIMARY KEY AUTO_INCREMENT,
    greenhouse_id INT NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    ubicacion VARCHAR(100),
    estado_actuador VARCHAR(20) DEFAULT 'inactivo',
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (greenhouse_id) REFERENCES greenhouses(id) ON DELETE CASCADE
);

-- =====================================================
-- 14. TABLA: actuator_controls
-- =====================================================
CREATE TABLE actuator_controls (
    id INT PRIMARY KEY AUTO_INCREMENT,
    actuator_id INT NOT NULL,
    usuario_id INT,
    accion VARCHAR(30) NOT NULL,
    valor_ajuste VARCHAR(50),
    resultado VARCHAR(20) DEFAULT 'exitoso',
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (actuator_id) REFERENCES actuators(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE SET NULL
);

-- =====================================================
-- 15. TABLA: greenhouse_settings
-- =====================================================
CREATE TABLE greenhouse_settings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    greenhouse_id INT NOT NULL UNIQUE,
    temp_min DECIMAL(5,2) DEFAULT 15.00,
    temp_max DECIMAL(5,2) DEFAULT 30.00,
    humedad_min DECIMAL(5,2) DEFAULT 40.00,
    humedad_max DECIMAL(5,2) DEFAULT 80.00,
    luz_min DECIMAL(10,2) DEFAULT 100.00,
    ph_min DECIMAL(4,2) DEFAULT 5.50,
    ph_max DECIMAL(4,2) DEFAULT 7.00,
    intervalo_lectura_minutos INT DEFAULT 15,
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (greenhouse_id) REFERENCES greenhouses(id) ON DELETE CASCADE
);

-- =====================================================
-- 16. TABLA: sensores_externos
-- =====================================================
CREATE TABLE sensores_externos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tipo VARCHAR(100) NOT NULL,
    valor_actual DECIMAL(10,2),
    ubicacion VARCHAR(255),
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- =====================================================
-- 17. TABLA: lecturas_externas
-- =====================================================
CREATE TABLE lecturas_externas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sensor_id INT,
    valor DECIMAL(10,2) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (sensor_id) REFERENCES sensores_externos(id) ON DELETE CASCADE
);

-- =====================================================
-- 18. TABLA: alertas_externas
-- =====================================================
CREATE TABLE alertas_externas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    mensaje TEXT NOT NULL,
    prioridad VARCHAR(20) DEFAULT 'media',
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
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
