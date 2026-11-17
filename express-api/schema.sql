CREATE TABLE IF NOT EXISTS sensores_externos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(100) NOT NULL,
    valor_actual DECIMAL(10, 2),
    ubicacion VARCHAR(255),
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS lecturas_externas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sensor_id INT,
    valor DECIMAL(10, 2) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (sensor_id) REFERENCES sensores_externos(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS alertas_externas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mensaje TEXT NOT NULL,
    prioridad VARCHAR(20) DEFAULT 'media',
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO sensores_externos (tipo, valor_actual, ubicacion) VALUES
('temperatura', 17.89, 'Estacion meteorologica - Cajica'),
('precipitacion', 2.72, 'Pluviometro - Chia'),
('viento', 8.16, 'Anemometro - Sopo'),
('humedad', 57.68, 'Higrometro exterior - Tenjo'),
('radiacion', 551.91, 'Radiometro solar - Zipaquira'),
('temperatura', 18.39, 'Estacion meteorologica - La Ceja'),
('precipitacion', 1.04, 'Pluviometro - Rionegro'),
('viento', 6.58, 'Anemometro - Marinilla'),
('humedad', 56.39, 'Higrometro exterior - Palmira'),
('radiacion', 475.23, 'Radiometro solar - Tulua'),
('temperatura', 14.84, 'Estacion meteorologica - Buga'),
('precipitacion', 1.63, 'Pluviometro - Cartago'),
('viento', 5.67, 'Anemometro - Ibague'),
('humedad', 85.59, 'Higrometro exterior - Espinal'),
('radiacion', 242.85, 'Radiometro solar - Tunja'),
('temperatura', 16.68, 'Estacion meteorologica - Duitama'),
('precipitacion', 11.29, 'Pluviometro - Sogamoso'),
('viento', 11.42, 'Anemometro - Villavicencio'),
('humedad', 76.35, 'Higrometro exterior - Facatativa'),
('radiacion', 447.51, 'Radiometro solar - El Penol');

INSERT INTO lecturas_externas (sensor_id, valor, timestamp) VALUES
(1, 19.8, '2026-10-20 06:00:00'),
(2, 0.91, '2026-10-21 07:13:00'),
(3, 9.59, '2026-10-22 08:26:00'),
(4, 56.84, '2026-10-23 09:39:00'),
(5, 550.49, '2026-10-24 10:52:00'),
(6, 16.86, '2026-10-25 11:05:00'),
(7, 0.27, '2026-10-26 12:18:00'),
(8, 7.84, '2026-10-27 13:31:00'),
(9, 55.11, '2026-10-28 14:44:00'),
(10, 475.56, '2026-10-29 15:57:00'),
(11, 15.4, '2026-10-20 16:10:00'),
(12, 1.12, '2026-10-21 17:23:00'),
(13, 5.86, '2026-10-22 18:36:00'),
(14, 83.84, '2026-10-23 19:49:00'),
(15, 241.09, '2026-10-24 06:02:00'),
(16, 15.5, '2026-10-25 07:15:00'),
(17, 12.01, '2026-10-26 08:28:00'),
(18, 11.13, '2026-10-27 09:41:00'),
(19, 75.61, '2026-10-28 10:54:00'),
(20, 447.85, '2026-10-29 11:07:00');

INSERT INTO alertas_externas (mensaje, prioridad) VALUES
('Lluvia intensa prevista: cerrar ventanas cenitales - Cajica', 'alta'),
('Viento fuerte sobre 10 m/s en la zona - Chia', 'alta'),
('Helada probable en la madrugada - Sopo', 'alta'),
('Radiacion solar muy alta: activar malla de sombra - Tenjo', 'media'),
('Humedad exterior superior al 90% - Zipaquira', 'media'),
('Sensor externo sin reportar en 30 minutos - La Ceja', 'media'),
('Bateria baja en estacion meteorologica - Rionegro', 'baja'),
('Calibracion pendiente del pluviometro - Marinilla', 'baja'),
('Lluvia intensa prevista: cerrar ventanas cenitales - Palmira', 'alta'),
('Viento fuerte sobre 10 m/s en la zona - Tulua', 'alta'),
('Helada probable en la madrugada - Buga', 'alta'),
('Radiacion solar muy alta: activar malla de sombra - Cartago', 'media'),
('Humedad exterior superior al 90% - Ibague', 'media'),
('Sensor externo sin reportar en 30 minutos - Espinal', 'media'),
('Bateria baja en estacion meteorologica - Tunja', 'baja'),
('Calibracion pendiente del pluviometro - Duitama', 'baja'),
('Lluvia intensa prevista: cerrar ventanas cenitales - Sogamoso', 'alta'),
('Viento fuerte sobre 10 m/s en la zona - Villavicencio', 'alta'),
('Helada probable en la madrugada - Facatativa', 'alta'),
('Radiacion solar muy alta: activar malla de sombra - El Penol', 'media');

