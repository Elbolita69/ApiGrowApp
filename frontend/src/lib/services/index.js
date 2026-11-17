export { request, BASE_FASTAPI, BASE_EXPRESS } from './api.js';

export * as auth from './auth.js';
export * as greenhouses from './greenhouses.js';
export * as sensors from './sensors.js';
export * as sensorReadings from './sensorReadings.js';
export * as crops from './crops.js';
export * as cropBatches from './cropBatches.js';
export * as alerts from './alerts.js';
export * as irrigationZones from './irrigationZones.js';
export * as irrigationLogs from './irrigationLogs.js';
export * as actuators from './actuators.js';
export * as actuatorControls from './actuatorControls.js';
export * as greenhouseSettings from './greenhouseSettings.js';
export * as users from './users.js';
export * as roles from './roles.js';
export * as estudiantes from './estudiantes.js';
export * as externos from './externos.js';
export * as asistente from './asistente.js';

import * as auth from './auth.js';
import * as greenhouses from './greenhouses.js';
import * as sensors from './sensors.js';
import * as sensorReadings from './sensorReadings.js';
import * as crops from './crops.js';
import * as cropBatches from './cropBatches.js';
import * as alerts from './alerts.js';
import * as irrigationZones from './irrigationZones.js';
import * as irrigationLogs from './irrigationLogs.js';
import * as actuators from './actuators.js';
import * as actuatorControls from './actuatorControls.js';
import * as greenhouseSettings from './greenhouseSettings.js';
import * as users from './users.js';
import * as roles from './roles.js';
import * as estudiantes from './estudiantes.js';
import * as externos from './externos.js';

export const serviciosPorModulo = {
	greenhouses,
	sensors,
	sensor_readings: sensorReadings,
	crops,
	crop_batches: cropBatches,
	alerts,
	irrigation_zones: irrigationZones,
	irrigation_logs: irrigationLogs,
	actuators,
	actuator_controls: actuatorControls,
	greenhouse_settings: greenhouseSettings,
	usuario: users,
	usuarios: users,
	roles,
	estudiantes,
	sensores_externos: externos.sensores,
	lecturas_externas: externos.lecturas,
	alertas_externas: externos.alertas
};
