-- =====================================================
-- MYSQL - Grow A Garden API (Express)
-- Para usar en bddiagram.io
-- 3 TABLAS
-- =====================================================

-- =====================================================
-- TABLA 1: sensores_externos
-- =====================================================
CREATE TABLE sensores_externos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(100) NOT NULL,
    valor_actual DECIMAL(10,2),
    ubicacion VARCHAR(255),
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_tipo_ubicacion (tipo, ubicacion)
);

-- =====================================================
-- TABLA 2: lecturas_externas
-- =====================================================
CREATE TABLE lecturas_externas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sensor_id INT,
    valor DECIMAL(10,2) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (sensor_id) REFERENCES sensores_externos(id) ON DELETE CASCADE,
    UNIQUE KEY unique_sensor_timestamp (sensor_id, timestamp)
);

-- =====================================================
-- TABLA 3: alertas_externas (SIN RELACIONES)
-- =====================================================
CREATE TABLE alertas_externas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo_alerta VARCHAR(50) NOT NULL UNIQUE,
    mensaje TEXT NOT NULL,
    prioridad VARCHAR(20) DEFAULT 'media',
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
