import { request } from './api.js';

const EXPRESS = { base: 'express' };

const cuerpoExpress = (datos) =>
	Object.fromEntries(
		Object.entries(datos ?? {}).map(([campo, valor]) => [
			campo,
			valor === '' || valor === undefined ? null : valor
		])
	);

async function listarSensores() {
	return request('/sensores-externos', EXPRESS);
}
async function obtenerSensor(id) {
	return request(`/sensores-externos/${id}`, EXPRESS);
}
async function crearSensor(datos) {
	return request('/sensores-externos', { ...EXPRESS, method: 'POST', body: cuerpoExpress(datos) });
}
async function actualizarSensor(id, datos) {
	return request(`/sensores-externos/${id}`, { ...EXPRESS, method: 'PUT', body: cuerpoExpress(datos) });
}
async function eliminarSensor(id) {
	return request(`/sensores-externos/${id}`, { ...EXPRESS, method: 'DELETE' });
}

async function listarLecturas() {
	return request('/lecturas-externas', EXPRESS);
}
async function obtenerLectura(id) {
	return request(`/lecturas-externas/${id}`, EXPRESS);
}
async function crearLectura(datos) {
	return request('/lecturas-externas', { ...EXPRESS, method: 'POST', body: cuerpoExpress(datos) });
}
async function actualizarLectura(id, datos) {
	return request(`/lecturas-externas/${id}`, { ...EXPRESS, method: 'PUT', body: cuerpoExpress(datos) });
}
async function eliminarLectura(id) {
	return request(`/lecturas-externas/${id}`, { ...EXPRESS, method: 'DELETE' });
}

async function listarAlertas() {
	return request('/alertas-externas', EXPRESS);
}
async function obtenerAlerta(id) {
	return request(`/alertas-externas/${id}`, EXPRESS);
}
async function crearAlerta(datos) {
	return request('/alertas-externas', { ...EXPRESS, method: 'POST', body: cuerpoExpress(datos) });
}
async function actualizarAlerta(id, datos) {
	return request(`/alertas-externas/${id}`, { ...EXPRESS, method: 'PUT', body: cuerpoExpress(datos) });
}
async function eliminarAlerta(id) {
	return request(`/alertas-externas/${id}`, { ...EXPRESS, method: 'DELETE' });
}

export const sensores = {
	listar: listarSensores,
	obtener: obtenerSensor,
	crear: crearSensor,
	actualizar: actualizarSensor,
	eliminar: eliminarSensor
};

export const lecturas = {
	listar: listarLecturas,
	obtener: obtenerLectura,
	crear: crearLectura,
	actualizar: actualizarLectura,
	eliminar: eliminarLectura
};

export const alertas = {
	listar: listarAlertas,
	obtener: obtenerAlerta,
	crear: crearAlerta,
	actualizar: actualizarAlerta,
	eliminar: eliminarAlerta
};

export const listar = listarSensores;
export const obtener = obtenerSensor;
export const crear = crearSensor;
export const actualizar = actualizarSensor;
export const eliminar = eliminarSensor;
