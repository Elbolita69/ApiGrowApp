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
DROP TABLE IF EXISTS moduloxrol CASCADE;
DROP TABLE IF EXISTS usuario CASCADE;
DROP TABLE IF EXISTS modulo CASCADE;
DROP TABLE IF EXISTS rol CASCADE;
DROP TABLE IF EXISTS greenhouses CASCADE;

CREATE TABLE rol (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion VARCHAR(200),
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE modulo (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion VARCHAR(200),
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

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

CREATE TABLE sensor_readings (
    id SERIAL PRIMARY KEY,
    sensor_id INTEGER NOT NULL REFERENCES sensors(id) ON DELETE CASCADE,
    valor NUMERIC(10,4) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

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

CREATE TABLE irrigation_logs (
    id SERIAL PRIMARY KEY,
    zone_id INTEGER NOT NULL REFERENCES irrigation_zones(id) ON DELETE CASCADE,
    duracion_minutos INTEGER NOT NULL,
    cantidad_agua_litros NUMERIC(10,2),
    modo VARCHAR(20) DEFAULT 'automatico',
    resultado VARCHAR(20) DEFAULT 'exitoso',
    notas TEXT,
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

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

-- Mantiene el campo "actualizado" automaticamente en cada UPDATE
CREATE OR REPLACE FUNCTION set_actualizado() RETURNS TRIGGER AS $$
BEGIN
    NEW.actualizado = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_rol_actualizado BEFORE UPDATE ON rol FOR EACH ROW EXECUTE FUNCTION set_actualizado();
CREATE TRIGGER trg_modulo_actualizado BEFORE UPDATE ON modulo FOR EACH ROW EXECUTE FUNCTION set_actualizado();
CREATE TRIGGER trg_moduloxrol_actualizado BEFORE UPDATE ON moduloxrol FOR EACH ROW EXECUTE FUNCTION set_actualizado();
CREATE TRIGGER trg_greenhouses_actualizado BEFORE UPDATE ON greenhouses FOR EACH ROW EXECUTE FUNCTION set_actualizado();
CREATE TRIGGER trg_usuario_actualizado BEFORE UPDATE ON usuario FOR EACH ROW EXECUTE FUNCTION set_actualizado();
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

CREATE INDEX idx_sensor_readings_sensor_id ON sensor_readings(sensor_id);
CREATE INDEX idx_sensor_readings_timestamp ON sensor_readings(timestamp DESC);
CREATE INDEX idx_alerts_greenhouse_id ON alerts(greenhouse_id);
CREATE INDEX idx_alerts_estado ON alerts(estado_alerta);
CREATE INDEX idx_crop_batches_estado ON crop_batches(estado_cultivo);
CREATE INDEX idx_irrigation_logs_zone_id ON irrigation_logs(zone_id);
CREATE INDEX idx_actuator_controls_actuator_id ON actuator_controls(actuator_id);
CREATE INDEX idx_usuario_username ON usuario(username);
CREATE INDEX idx_usuario_email ON usuario(email);

-- =====================  DATOS INICIALES  =====================
-- Contrasenas de prueba: admin -> Admin123*  | operadores -> Operador123*  | agronomos -> Agronomo123*

-- =====================  DATOS INICIALES  =====================
-- Contrasenas de prueba: admin -> Admin123*  | operadores -> Operador123*  | agronomos -> Agronomo123*

INSERT INTO rol (nombre, descripcion) VALUES
('administrador', 'Administra todo el sistema, usuarios y configuracion'),
('operador', 'Opera sensores, actuadores y riego del invernadero'),
('agronomo', 'Gestiona cultivos, lotes, alertas y parametros agronomicos');

INSERT INTO modulo (nombre, descripcion) VALUES
('greenhouses', 'Invernaderos'),
('sensors', 'Sensores'),
('sensor_readings', 'Lecturas de sensores'),
('crops', 'Catalogo de cultivos'),
('crop_batches', 'Lotes de cultivo'),
('alerts', 'Alertas'),
('irrigation_zones', 'Zonas de riego'),
('irrigation_logs', 'Historial de riego'),
('actuators', 'Actuadores'),
('actuator_controls', 'Control de actuadores'),
('greenhouse_settings', 'Parametros del invernadero'),
('usuario', 'Usuarios'),
('sensores_externos', 'Sensores externos'),
('lecturas_externas', 'Lecturas externas'),
('alertas_externas', 'Alertas externas');

INSERT INTO moduloxrol (rol_id, modulo_id, puede_ver, puede_crear, puede_editar, puede_eliminar) VALUES
(1, 1, True, True, True, True),
(1, 2, True, True, True, True),
(1, 3, True, True, True, True),
(1, 4, True, True, True, True),
(1, 5, True, True, True, True),
(1, 6, True, True, True, True),
(1, 7, True, True, True, True),
(1, 8, True, True, True, True),
(1, 9, True, True, True, True),
(1, 10, True, True, True, True),
(1, 11, True, True, True, True),
(1, 12, True, True, True, True),
(1, 13, True, True, True, True),
(1, 14, True, True, True, True),
(1, 15, True, True, True, True),
(2, 1, True, False, False, False),
(2, 2, True, True, True, True),
(2, 3, True, True, True, True),
(2, 9, True, True, True, True),
(2, 10, True, True, True, True),
(2, 7, True, True, True, True),
(2, 8, True, True, True, True),
(2, 6, True, False, True, False),
(2, 13, True, True, True, True),
(3, 1, True, False, False, False),
(3, 2, True, False, False, False),
(3, 3, True, False, False, False),
(3, 4, True, True, True, True),
(3, 5, True, True, True, True),
(3, 11, True, True, True, True),
(3, 6, True, True, True, True),
(3, 14, True, True, True, True),
(3, 15, True, True, True, True);

INSERT INTO greenhouses (nombre, ubicacion, area_metros_cuadrados, capacidad_maxima) VALUES
('Invernadero Tomate Chonto Cajica', 'Cajica, Cundinamarca', 1200, 6000),
('Invernadero Lechugas Chia', 'Chia, Cundinamarca', 800, 9000),
('Invernadero Fresas Sopo', 'Sopo, Cundinamarca', 650, 7500),
('Invernadero Pimenton Facatativa', 'Facatativa, Cundinamarca', 900, 4500),
('Invernadero Pepino Tenjo', 'Tenjo, Cundinamarca', 700, 3500),
('Invernadero Flores Zipaquira', 'Zipaquira, Cundinamarca', 1500, 12000),
('Invernadero Aromaticas La Ceja', 'La Ceja, Antioquia', 500, 5000),
('Invernadero Tomate Rionegro', 'Rionegro, Antioquia', 1100, 5500),
('Invernadero Mora Marinilla', 'Marinilla, Antioquia', 600, 2400),
('Invernadero Hortalizas El Penol', 'El Penol, Antioquia', 750, 6000),
('Invernadero Tomate Palmira', 'Palmira, Valle del Cauca', 1300, 6500),
('Invernadero Pimenton Tulua', 'Tulua, Valle del Cauca', 950, 4750),
('Invernadero Lechuga Buga', 'Buga, Valle del Cauca', 700, 8400),
('Invernadero Cebolla Cartago', 'Cartago, Valle del Cauca', 850, 12000),
('Invernadero Tomate Ibague', 'Ibague, Tolima', 1000, 5000),
('Invernadero Pepino Espinal', 'Espinal, Tolima', 780, 3900),
('Invernadero Fresas Tunja', 'Tunja, Boyaca', 560, 6720),
('Invernadero Habichuela Duitama', 'Duitama, Boyaca', 640, 7680),
('Invernadero Tomate Sogamoso', 'Sogamoso, Boyaca', 900, 4500),
('Invernadero Aji Villavicencio', 'Villavicencio, Meta', 720, 3600);

INSERT INTO crops (nombre, nombre_cientifico, temperatura_min, temperatura_max, humedad_min, humedad_max, ph_min, ph_max, ciclo_dias) VALUES
('Tomate chonto', 'Solanum lycopersicum', 18, 27, 60, 80, 5.5, 6.8, 110),
('Lechuga batavia', 'Lactuca sativa', 10, 20, 70, 90, 5.8, 6.6, 55),
('Fresa', 'Fragaria x ananassa', 15, 25, 65, 80, 5.5, 6.5, 120),
('Pimenton', 'Capsicum annuum', 18, 28, 50, 70, 5.8, 6.8, 95),
('Pepino cohombro', 'Cucumis sativus', 20, 30, 75, 90, 5.5, 6.8, 65),
('Cebolla larga', 'Allium fistulosum', 12, 24, 60, 80, 6.0, 7.0, 100),
('Mora de Castilla', 'Rubus glaucus', 14, 22, 70, 85, 5.5, 6.5, 240),
('Habichuela', 'Phaseolus vulgaris', 16, 27, 60, 75, 6.0, 7.0, 70),
('Aji', 'Capsicum baccatum', 20, 30, 55, 75, 6.0, 7.0, 100),
('Cilantro', 'Coriandrum sativum', 12, 22, 60, 75, 6.2, 6.8, 45),
('Perejil', 'Petroselinum crispum', 12, 22, 60, 75, 6.0, 7.0, 70),
('Albahaca', 'Ocimum basilicum', 18, 28, 60, 75, 6.0, 7.0, 60),
('Espinaca', 'Spinacia oleracea', 8, 20, 65, 85, 6.0, 7.5, 50),
('Acelga', 'Beta vulgaris var. cicla', 10, 24, 65, 80, 6.0, 7.5, 60),
('Zanahoria', 'Daucus carota', 12, 24, 60, 80, 6.0, 6.8, 100),
('Rabano', 'Raphanus sativus', 10, 22, 65, 80, 6.0, 7.0, 30),
('Brocoli', 'Brassica oleracea var. italica', 12, 22, 65, 85, 6.0, 7.0, 90),
('Coliflor', 'Brassica oleracea var. botrytis', 12, 22, 65, 85, 6.0, 7.0, 100),
('Calabacin', 'Cucurbita pepo', 18, 28, 60, 75, 6.0, 7.0, 55),
('Apio', 'Apium graveolens', 12, 22, 70, 85, 6.0, 7.0, 110);

INSERT INTO usuario (username, email, password_hash, nombre, rol_id) VALUES
('admin', 'admin@growapp.co', '$2b$10$8U.JUpTVKLignM8WNub6D.f44rMv07zclp4MxpX5wthCLpvO3UdHq', 'Carlos Andres Ramirez', 1),
('operador1', 'operador1@growapp.co', '$2b$10$ttkQcZ.9Tuobmhcat0Eme.4VfJJF1AFwv8UdP.4tQlaCHsajtFvaq', 'Juan Pablo Rojas', 2),
('operador2', 'operador2@growapp.co', '$2b$10$ttkQcZ.9Tuobmhcat0Eme.4VfJJF1AFwv8UdP.4tQlaCHsajtFvaq', 'Maria Fernanda Gomez', 2),
('operador3', 'operador3@growapp.co', '$2b$10$ttkQcZ.9Tuobmhcat0Eme.4VfJJF1AFwv8UdP.4tQlaCHsajtFvaq', 'Luis Alberto Castro', 2),
('operador4', 'operador4@growapp.co', '$2b$10$ttkQcZ.9Tuobmhcat0Eme.4VfJJF1AFwv8UdP.4tQlaCHsajtFvaq', 'Diana Carolina Pardo', 2),
('operador5', 'operador5@growapp.co', '$2b$10$ttkQcZ.9Tuobmhcat0Eme.4VfJJF1AFwv8UdP.4tQlaCHsajtFvaq', 'Andres Felipe Mejia', 2),
('operador6', 'operador6@growapp.co', '$2b$10$ttkQcZ.9Tuobmhcat0Eme.4VfJJF1AFwv8UdP.4tQlaCHsajtFvaq', 'Laura Sofia Herrera', 2),
('operador7', 'operador7@growapp.co', '$2b$10$ttkQcZ.9Tuobmhcat0Eme.4VfJJF1AFwv8UdP.4tQlaCHsajtFvaq', 'Jorge Enrique Vargas', 2),
('operador8', 'operador8@growapp.co', '$2b$10$ttkQcZ.9Tuobmhcat0Eme.4VfJJF1AFwv8UdP.4tQlaCHsajtFvaq', 'Paola Andrea Cruz', 2),
('operador9', 'operador9@growapp.co', '$2b$10$ttkQcZ.9Tuobmhcat0Eme.4VfJJF1AFwv8UdP.4tQlaCHsajtFvaq', 'Camilo Ernesto Ortiz', 2),
('operador10', 'operador10@growapp.co', '$2b$10$ttkQcZ.9Tuobmhcat0Eme.4VfJJF1AFwv8UdP.4tQlaCHsajtFvaq', 'Natalia Rocio Salazar', 2),
('agronomo1', 'agronomo1@growapp.co', '$2b$10$66DFKqXuA3DoJebuy9tSjOpbLM4w4ZkszDrMCaKQBSq23BD365M.O', 'Sandra Milena Torres', 3),
('agronomo2', 'agronomo2@growapp.co', '$2b$10$66DFKqXuA3DoJebuy9tSjOpbLM4w4ZkszDrMCaKQBSq23BD365M.O', 'Ricardo Alonso Beltran', 3),
('agronomo3', 'agronomo3@growapp.co', '$2b$10$66DFKqXuA3DoJebuy9tSjOpbLM4w4ZkszDrMCaKQBSq23BD365M.O', 'Claudia Patricia Mendoza', 3),
('agronomo4', 'agronomo4@growapp.co', '$2b$10$66DFKqXuA3DoJebuy9tSjOpbLM4w4ZkszDrMCaKQBSq23BD365M.O', 'Hector Fabian Rincon', 3),
('agronomo5', 'agronomo5@growapp.co', '$2b$10$66DFKqXuA3DoJebuy9tSjOpbLM4w4ZkszDrMCaKQBSq23BD365M.O', 'Viviana Alejandra Leon', 3),
('agronomo6', 'agronomo6@growapp.co', '$2b$10$66DFKqXuA3DoJebuy9tSjOpbLM4w4ZkszDrMCaKQBSq23BD365M.O', 'Daniel Esteban Acosta', 3),
('agronomo7', 'agronomo7@growapp.co', '$2b$10$66DFKqXuA3DoJebuy9tSjOpbLM4w4ZkszDrMCaKQBSq23BD365M.O', 'Monica Lucia Forero', 3),
('agronomo8', 'agronomo8@growapp.co', '$2b$10$66DFKqXuA3DoJebuy9tSjOpbLM4w4ZkszDrMCaKQBSq23BD365M.O', 'Oscar Mauricio Duarte', 3),
('agronomo9', 'agronomo9@growapp.co', '$2b$10$66DFKqXuA3DoJebuy9tSjOpbLM4w4ZkszDrMCaKQBSq23BD365M.O', 'Angela Maria Silva', 3);

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

INSERT INTO sensor_readings (sensor_id, valor, timestamp) VALUES
(1, 19.19, '2026-10-20 06:00:00'),
(1, 23.03, '2026-10-25 13:00:00'),
(2, 70.35, '2026-10-21 09:07:00'),
(2, 80.8, '2026-10-26 16:07:00'),
(3, 5.73, '2026-10-22 12:14:00'),
(3, 5.89, '2026-10-27 19:14:00'),
(4, 22424.74, '2026-10-20 15:21:00'),
(4, 21357.42, '2026-10-25 08:21:00'),
(5, 791.69, '2026-10-21 18:28:00'),
(5, 673.91, '2026-10-26 11:28:00'),
(6, 25.31, '2026-10-22 07:35:00'),
(6, 25.68, '2026-10-27 14:35:00'),
(7, 77.53, '2026-10-20 10:42:00'),
(7, 72.6, '2026-10-25 17:42:00'),
(8, 5.91, '2026-10-21 13:49:00'),
(8, 6.4, '2026-10-26 06:49:00'),
(9, 10657.68, '2026-10-22 16:56:00'),
(9, 27602.27, '2026-10-27 09:56:00'),
(10, 624.83, '2026-10-20 19:03:00'),
(10, 807.38, '2026-10-25 12:03:00'),
(11, 24.85, '2026-10-21 08:10:00'),
(11, 24.79, '2026-10-26 15:10:00'),
(12, 61.31, '2026-10-22 11:17:00'),
(12, 62.55, '2026-10-27 18:17:00'),
(13, 6.87, '2026-10-20 14:24:00'),
(13, 6.81, '2026-10-25 07:24:00'),
(14, 27323.26, '2026-10-21 17:31:00'),
(14, 31991.75, '2026-10-26 10:31:00'),
(15, 656.79, '2026-10-22 06:38:00'),
(15, 438.16, '2026-10-27 13:38:00'),
(16, 21.4, '2026-10-20 09:45:00'),
(16, 23.57, '2026-10-25 16:45:00'),
(17, 63.76, '2026-10-21 12:52:00'),
(17, 68.72, '2026-10-26 19:52:00'),
(18, 6.74, '2026-10-22 15:59:00'),
(18, 6.52, '2026-10-27 08:59:00'),
(19, 21858.16, '2026-10-20 18:06:00'),
(19, 8593.74, '2026-10-25 11:06:00'),
(20, 755.43, '2026-10-21 07:13:00'),
(20, 581.77, '2026-10-26 14:13:00');

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

INSERT INTO alerts (greenhouse_id, sensor_id, tipo, mensaje, valor_actual, umbral, prioridad, estado_alerta, resuelta_en) VALUES
(1, 1, 'temperatura_alta', 'Temperatura por encima del maximo permitido (Cajica)', 32.23, 28, 'alta', 'activa', NULL),
(2, 2, 'humedad_baja', 'Humedad relativa por debajo del minimo (Chia)', 49.3, 55, 'media', 'activa', NULL),
(3, 3, 'ph_fuera_rango', 'pH del suelo fuera del rango optimo (Sopo)', 8.85, 6.9, 'media', 'reconocida', NULL),
(4, 4, 'co2_alto', 'Concentracion de CO2 elevada (Facatativa)', 1101.89, 900, 'baja', 'resuelta', '2026-10-28 10:30:00'),
(5, 5, 'luz_baja', 'Luminosidad insuficiente para el cultivo (Tenjo)', 5200.57, 8000, 'baja', 'activa', NULL),
(6, 6, 'temperatura_alta', 'Temperatura por encima del maximo permitido (Zipaquira)', 32.51, 28, 'alta', 'activa', NULL),
(7, 7, 'humedad_baja', 'Humedad relativa por debajo del minimo (La Ceja)', 49.15, 55, 'media', 'reconocida', NULL),
(8, 8, 'ph_fuera_rango', 'pH del suelo fuera del rango optimo (Rionegro)', 7.69, 6.9, 'media', 'resuelta', '2026-10-28 10:30:00'),
(9, 9, 'co2_alto', 'Concentracion de CO2 elevada (Marinilla)', 1099.43, 900, 'baja', 'activa', NULL),
(10, 10, 'luz_baja', 'Luminosidad insuficiente para el cultivo (El Penol)', 5201.65, 8000, 'baja', 'activa', NULL),
(11, 11, 'temperatura_alta', 'Temperatura por encima del maximo permitido (Palmira)', 33.05, 28, 'alta', 'reconocida', NULL),
(12, 12, 'humedad_baja', 'Humedad relativa por debajo del minimo (Tulua)', 47.37, 55, 'media', 'resuelta', '2026-10-28 10:30:00'),
(13, 13, 'ph_fuera_rango', 'pH del suelo fuera del rango optimo (Buga)', 8.5, 6.9, 'media', 'activa', NULL),
(14, 14, 'co2_alto', 'Concentracion de CO2 elevada (Cartago)', 1101.02, 900, 'baja', 'activa', NULL),
(15, 15, 'luz_baja', 'Luminosidad insuficiente para el cultivo (Ibague)', 5201.14, 8000, 'baja', 'reconocida', NULL),
(16, 16, 'temperatura_alta', 'Temperatura por encima del maximo permitido (Espinal)', 33.38, 28, 'alta', 'resuelta', '2026-10-28 10:30:00'),
(17, 17, 'humedad_baja', 'Humedad relativa por debajo del minimo (Tunja)', 49.94, 55, 'media', 'activa', NULL),
(18, 18, 'ph_fuera_rango', 'pH del suelo fuera del rango optimo (Duitama)', 7.15, 6.9, 'media', 'activa', NULL),
(19, 19, 'co2_alto', 'Concentracion de CO2 elevada (Sogamoso)', 1100.21, 900, 'baja', 'reconocida', NULL),
(20, 20, 'luz_baja', 'Luminosidad insuficiente para el cultivo (Villavicencio)', 5201.99, 8000, 'baja', 'resuelta', '2026-10-28 10:30:00');

INSERT INTO irrigation_zones (greenhouse_id, nombre, capacidad_litros_min, capacidad_litros_max, tipo) VALUES
(1, 'Sector A - Tomate chonto', 80, 300, 'gotas'),
(2, 'Sector B - Lechuga batavia', 100, 360, 'aspersion'),
(3, 'Sector C - Fresa', 120, 420, 'microaspersion'),
(4, 'Sector D - Pimenton', 140, 480, 'gotas'),
(5, 'Sector A - Pepino cohombro', 160, 540, 'aspersion'),
(6, 'Sector B - Cebolla larga', 80, 300, 'microaspersion'),
(7, 'Sector C - Mora de Castilla', 100, 360, 'gotas'),
(8, 'Sector D - Habichuela', 120, 420, 'aspersion'),
(9, 'Sector A - Aji', 140, 480, 'microaspersion'),
(10, 'Sector B - Cilantro', 160, 540, 'gotas'),
(11, 'Sector C - Perejil', 80, 300, 'aspersion'),
(12, 'Sector D - Albahaca', 100, 360, 'microaspersion'),
(13, 'Sector A - Espinaca', 120, 420, 'gotas'),
(14, 'Sector B - Acelga', 140, 480, 'aspersion'),
(15, 'Sector C - Zanahoria', 160, 540, 'microaspersion'),
(16, 'Sector D - Rabano', 80, 300, 'gotas'),
(17, 'Sector A - Brocoli', 100, 360, 'aspersion'),
(18, 'Sector B - Coliflor', 120, 420, 'microaspersion'),
(19, 'Sector C - Calabacin', 140, 480, 'gotas'),
(20, 'Sector D - Apio', 160, 540, 'aspersion');

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

INSERT INTO actuator_controls (actuator_id, usuario_id, accion, valor_ajuste, resultado) VALUES
(1, 2, 'abrir', '100%', 'fallido'),
(2, 3, 'cerrar', '0%', 'exitoso'),
(3, 4, 'encender', NULL, 'exitoso'),
(4, 5, 'apagar', NULL, 'exitoso'),
(5, 6, 'ajustar', '60%', 'exitoso'),
(6, 7, 'abrir', '100%', 'exitoso'),
(7, 8, 'cerrar', '0%', 'exitoso'),
(8, 9, 'encender', NULL, 'fallido'),
(9, 10, 'apagar', NULL, 'exitoso'),
(10, 11, 'ajustar', '60%', 'exitoso'),
(11, 2, 'abrir', '100%', 'exitoso'),
(12, 3, 'cerrar', '0%', 'exitoso'),
(13, 4, 'encender', NULL, 'exitoso'),
(14, 5, 'apagar', NULL, 'exitoso'),
(15, 6, 'ajustar', '60%', 'fallido'),
(16, 7, 'abrir', '100%', 'exitoso'),
(17, 8, 'cerrar', '0%', 'exitoso'),
(18, 9, 'encender', NULL, 'exitoso'),
(19, 10, 'apagar', NULL, 'exitoso'),
(20, 11, 'ajustar', '60%', 'exitoso');

INSERT INTO greenhouse_settings (greenhouse_id, temp_min, temp_max, humedad_min, humedad_max, luz_min, ph_min, ph_max, intervalo_lectura_minutos) VALUES
(1, 18, 27, 60, 80, 8000, 5.5, 6.8, 15),
(2, 10, 20, 70, 90, 9000, 5.8, 6.6, 15),
(3, 15, 25, 65, 80, 10000, 5.5, 6.5, 15),
(4, 18, 28, 50, 70, 11000, 5.8, 6.8, 15),
(5, 20, 30, 75, 90, 8000, 5.5, 6.8, 15),
(6, 12, 24, 60, 80, 9000, 6.0, 7.0, 15),
(7, 14, 22, 70, 85, 10000, 5.5, 6.5, 15),
(8, 16, 27, 60, 75, 11000, 6.0, 7.0, 15),
(9, 20, 30, 55, 75, 8000, 6.0, 7.0, 15),
(10, 12, 22, 60, 75, 9000, 6.2, 6.8, 15),
(11, 12, 22, 60, 75, 10000, 6.0, 7.0, 15),
(12, 18, 28, 60, 75, 11000, 6.0, 7.0, 15),
(13, 8, 20, 65, 85, 8000, 6.0, 7.5, 15),
(14, 10, 24, 65, 80, 9000, 6.0, 7.5, 15),
(15, 12, 24, 60, 80, 10000, 6.0, 6.8, 15),
(16, 10, 22, 65, 80, 11000, 6.0, 7.0, 15),
(17, 12, 22, 65, 85, 8000, 6.0, 7.0, 15),
(18, 12, 22, 65, 85, 9000, 6.0, 7.0, 15),
(19, 18, 28, 60, 75, 10000, 6.0, 7.0, 15),
(20, 12, 22, 70, 85, 11000, 6.0, 7.0, 15);

