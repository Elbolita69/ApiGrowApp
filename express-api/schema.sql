-- Smart Greenhouse Auxiliary Database Schema (PostgreSQL)
-- Usar las mismas tablas de la base de datos principal o crear tablas adicionales

-- Tabla: sensores_externos
CREATE TABLE IF NOT EXISTS sensores_externos (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(100) NOT NULL,
    valor_actual NUMERIC(10, 2),
    ubicacion VARCHAR(255),
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: lecturas_externas
CREATE TABLE IF NOT EXISTS lecturas_externas (
    id SERIAL PRIMARY KEY,
    sensor_id INTEGER REFERENCES sensores_externos(id) ON DELETE CASCADE,
    valor NUMERIC(10, 2) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: alertas_externas
CREATE TABLE IF NOT EXISTS alertas_externas (
    id SERIAL PRIMARY KEY,
    mensaje TEXT NOT NULL,
    prioridad VARCHAR(20) DEFAULT 'media',
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Seed data inicial
INSERT INTO sensores_externos (tipo, valor_actual, ubicacion) VALUES
('temperatura', 25.50, 'Externo Norte'),
('humedad', 65.00, 'Externo Sur');

INSERT INTO alertas_externas (mensaje, prioridad) VALUES
('Sensor externo desconectado', 'alta');
