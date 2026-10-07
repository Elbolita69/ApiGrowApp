-- Smart Greenhouse Auxiliary Database Schema

CREATE DATABASE IF NOT EXISTS greenhouse_aux;
USE greenhouse_aux;

-- Tabla: sensores_externos
CREATE TABLE IF NOT EXISTS sensores_externos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(100) NOT NULL,
    valor_actual DECIMAL(10, 2),
    ubicacion VARCHAR(255),
    estado BOOLEAN DEFAULT TRUE,
    creado DATETIME DEFAULT CURRENT_TIMESTAMP,
    actualizado DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla: lecturas_externas
CREATE TABLE IF NOT EXISTS lecturas_externas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sensor_id INT NOT NULL,
    valor DECIMAL(10, 2) NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE,
    creado DATETIME DEFAULT CURRENT_TIMESTAMP,
    actualizado DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (sensor_id) REFERENCES sensores_externos(id) ON DELETE CASCADE
);

-- Tabla: alertas_externas
CREATE TABLE IF NOT EXISTS alertas_externas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mensaje TEXT NOT NULL,
    prioridad ENUM('baja', 'media', 'alta', 'critica') DEFAULT 'media',
    estado BOOLEAN DEFAULT TRUE,
    creado DATETIME DEFAULT CURRENT_TIMESTAMP,
    actualizado DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
