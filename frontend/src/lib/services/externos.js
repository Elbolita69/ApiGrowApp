// Servicios de la API auxiliar (Express + MySQL). No usa token: es otra base de datos.
// El proxy '/api-express' quita el prefijo y reenvia a http://localhost:3000.
import { request } from './api.js';

/** @type {{ base: 'express' }} */
const EXPRESS = { base: 'express' };

// Express exige todos los parametros: los vacios se envian como null.
/** @param {Record<string, any>} datos */
const cuerpoExpress = (datos) =>
	Object.fromEntries(
		Object.entries(datos ?? {}).map(([campo, valor]) => [
			campo,
			valor === '' || valor === undefined ? null : valor
		])
	);

// --- Sensores externos ---------------------------------------------------------
async function listarSensores() {
	return request('/sensores-externos', EXPRESS);
}
/** @param {number|string} id */
async function obtenerSensor(id) {
	return request(`/sensores-externos/${id}`, EXPRESS);
}
/** @param {Record<string, any>} datos */
async function crearSensor(datos) {
	return request('/sensores-externos', { ...EXPRESS, method: 'POST', body: cuerpoExpress(datos) });
}
/** @param {number|string} id @param {Record<string, any>} datos */
async function actualizarSensor(id, datos) {
	return request(`/sensores-externos/${id}`, { ...EXPRESS, method: 'PUT', body: cuerpoExpress(datos) });
}
/** @param {number|string} id */
async function eliminarSensor(id) {
	return request(`/sensores-externos/${id}`, { ...EXPRESS, method: 'DELETE' });
}

// --- Lecturas externas ---------------------------------------------------------
async function listarLecturas() {
	return request('/lecturas-externas', EXPRESS);
}
/** @param {number|string} id */
async function obtenerLectura(id) {
	return request(`/lecturas-externas/${id}`, EXPRESS);
}
/** @param {Record<string, any>} datos */
async function crearLectura(datos) {
	return request('/lecturas-externas', { ...EXPRESS, method: 'POST', body: cuerpoExpress(datos) });
}
/** @param {number|string} id @param {Record<string, any>} datos */
async function actualizarLectura(id, datos) {
	return request(`/lecturas-externas/${id}`, { ...EXPRESS, method: 'PUT', body: cuerpoExpress(datos) });
}
/** @param {number|string} id */
async function eliminarLectura(id) {
	return request(`/lecturas-externas/${id}`, { ...EXPRESS, method: 'DELETE' });
}

// --- Alertas externas ----------------------------------------------------------
async function listarAlertas() {
	return request('/alertas-externas', EXPRESS);
}
/** @param {number|string} id */
async function obtenerAlerta(id) {
	return request(`/alertas-externas/${id}`, EXPRESS);
}
/** @param {Record<string, any>} datos */
async function crearAlerta(datos) {
	return request('/alertas-externas', { ...EXPRESS, method: 'POST', body: cuerpoExpress(datos) });
}
/** @param {number|string} id @param {Record<string, any>} datos */
async function actualizarAlerta(id, datos) {
	return request(`/alertas-externas/${id}`, { ...EXPRESS, method: 'PUT', body: cuerpoExpress(datos) });
}
/** @param {number|string} id */
async function eliminarAlerta(id) {
	return request(`/alertas-externas/${id}`, { ...EXPRESS, method: 'DELETE' });
}

/** Sensores externos (estaciones meteorologicas). */
export const sensores = {
	listar: listarSensores,
	obtener: obtenerSensor,
	crear: crearSensor,
	actualizar: actualizarSensor,
	eliminar: eliminarSensor
};

/** Lecturas de los sensores externos. */
export const lecturas = {
	listar: listarLecturas,
	obtener: obtenerLectura,
	crear: crearLectura,
	actualizar: actualizarLectura,
	eliminar: eliminarLectura
};

/** Alertas generadas por la API auxiliar. */
export const alertas = {
	listar: listarAlertas,
	obtener: obtenerAlerta,
	crear: crearAlerta,
	actualizar: actualizarAlerta,
	eliminar: eliminarAlerta
};

// Atajos: el recurso principal de este archivo son los sensores externos.
export const listar = listarSensores;
export const obtener = obtenerSensor;
export const crear = crearSensor;
export const actualizar = actualizarSensor;
export const eliminar = eliminarSensor;
