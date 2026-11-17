export const LOOKUPS = {
	greenhouses: { servicio: 'greenhouses', label: 'nombre' },
	sensors: { servicio: 'sensors', label: 'nombre' },
	crops: { servicio: 'crops', label: 'nombre' },
	zones: { servicio: 'irrigation_zones', label: 'nombre' },
	actuators: { servicio: 'actuators', label: 'nombre' },
	roles: { servicio: 'roles', label: 'nombre' },
	sensoresExternos: { servicio: 'sensores_externos', label: 'ubicacion' }
};

const TIPOS_SENSOR = ['temperatura', 'humedad', 'ph', 'luz', 'co2'];

export const MODULOS = {
	greenhouses: {
		titulo: 'Invernaderos',
		singular: 'invernadero',
		icono: 'bi-house-gear',
		ruta: 'invernaderos',
		columnas: [
			{ key: 'nombre', label: 'Nombre' },
			{ key: 'ubicacion', label: 'Ubicacion' },
			{ key: 'area_metros_cuadrados', label: 'Area (m²)', tipo: 'numero' },
			{ key: 'capacidad_maxima', label: 'Capacidad (plantas)', tipo: 'numero' },
			{ key: 'actualizado', label: 'Actualizado', tipo: 'fechahora' }
		],
		campos: [
			{ key: 'nombre', label: 'Nombre', tipo: 'text', requerido: true },
			{ key: 'ubicacion', label: 'Ubicacion (municipio, departamento)', tipo: 'text' },
			{ key: 'area_metros_cuadrados', label: 'Area en m²', tipo: 'number', step: '0.01', min: 0 },
			{ key: 'capacidad_maxima', label: 'Capacidad maxima de plantas', tipo: 'number', step: '1', min: 0 }
		]
	},
	sensors: {
		titulo: 'Sensores',
		singular: 'sensor',
		icono: 'bi-thermometer-half',
		ruta: 'sensores',
		columnas: [
			{ key: 'nombre', label: 'Sensor' },
			{ key: 'tipo', label: 'Tipo', tipo: 'etiqueta' },
			{ key: 'greenhouse_id', label: 'Invernadero', lookup: 'greenhouses' },
			{ key: 'unidad', label: 'Unidad' },
			{ key: 'ubicacion', label: 'Ubicacion' },
			{ key: 'actualizado', label: 'Actualizado', tipo: 'fechahora' }
		],
		campos: [
			{ key: 'greenhouse_id', label: 'Invernadero', tipo: 'select', lookup: 'greenhouses', requerido: true },
			{ key: 'tipo', label: 'Tipo de sensor', tipo: 'select', opciones: TIPOS_SENSOR, requerido: true },
			{ key: 'nombre', label: 'Nombre del sensor', tipo: 'text', requerido: true },
			{ key: 'unidad', label: 'Unidad de medida (C, %, pH, lux, ppm)', tipo: 'text', requerido: true },
			{ key: 'ubicacion', label: 'Ubicacion dentro del invernadero', tipo: 'text' }
		]
	},
	sensor_readings: {
		titulo: 'Lecturas de sensores',
		singular: 'lectura',
		icono: 'bi-graph-up',
		ruta: 'lecturas',
		columnas: [
			{ key: 'sensor_nombre', label: 'Sensor' },
			{ key: 'tipo', label: 'Tipo', tipo: 'etiqueta' },
			{ key: 'valor', label: 'Valor', tipo: 'numero' },
			{ key: 'unidad', label: 'Unidad' },
			{ key: 'timestamp', label: 'Fecha de la lectura', tipo: 'fechahora' },
			{ key: 'actualizado', label: 'Actualizado', tipo: 'fechahora' }
		],
		campos: [
			{ key: 'sensor_id', label: 'Sensor', tipo: 'select', lookup: 'sensors', requerido: true },
			{ key: 'valor', label: 'Valor medido', tipo: 'number', step: '0.01', requerido: true }
		]
	},
	crops: {
		titulo: 'Cultivos',
		singular: 'cultivo',
		icono: 'bi-flower2',
		ruta: 'cultivos',
		columnas: [
			{ key: 'nombre', label: 'Cultivo' },
			{ key: 'nombre_cientifico', label: 'Nombre cientifico' },
			{ key: 'temperatura_min', label: 'T min (°C)', tipo: 'numero' },
			{ key: 'temperatura_max', label: 'T max (°C)', tipo: 'numero' },
			{ key: 'humedad_min', label: 'Hum. min (%)', tipo: 'numero' },
			{ key: 'humedad_max', label: 'Hum. max (%)', tipo: 'numero' },
			{ key: 'ciclo_dias', label: 'Ciclo (dias)', tipo: 'numero' },
			{ key: 'actualizado', label: 'Actualizado', tipo: 'fechahora' }
		],
		campos: [
			{ key: 'nombre', label: 'Nombre comun', tipo: 'text', requerido: true },
			{ key: 'nombre_cientifico', label: 'Nombre cientifico', tipo: 'text' },
			{ key: 'temperatura_min', label: 'Temperatura minima (°C)', tipo: 'number', step: '0.1' },
			{ key: 'temperatura_max', label: 'Temperatura maxima (°C)', tipo: 'number', step: '0.1' },
			{ key: 'humedad_min', label: 'Humedad minima (%)', tipo: 'number', step: '0.1' },
			{ key: 'humedad_max', label: 'Humedad maxima (%)', tipo: 'number', step: '0.1' },
			{ key: 'ph_min', label: 'pH minimo', tipo: 'number', step: '0.1' },
			{ key: 'ph_max', label: 'pH maximo', tipo: 'number', step: '0.1' },
			{ key: 'ciclo_dias', label: 'Ciclo del cultivo (dias)', tipo: 'number', step: '1', min: 1 },
			{ key: 'descripcion', label: 'Descripcion', tipo: 'textarea', ancho: 12 }
		]
	},
	crop_batches: {
		titulo: 'Lotes de cultivo',
		singular: 'lote',
		icono: 'bi-basket',
		ruta: 'lotes',
		columnas: [
			{ key: 'cultivo_nombre', label: 'Cultivo' },
			{ key: 'greenhouse_id', label: 'Invernadero', lookup: 'greenhouses' },
			{ key: 'fecha_siembra', label: 'Siembra', tipo: 'fecha' },
			{ key: 'fecha_cosecha_estimada', label: 'Cosecha estimada', tipo: 'fecha' },
			{ key: 'cantidad_plantas', label: 'Plantas', tipo: 'numero' },
			{ key: 'estado_cultivo', label: 'Estado del lote', tipo: 'etiqueta' },
			{ key: 'actualizado', label: 'Actualizado', tipo: 'fechahora' }
		],
		campos: [
			{ key: 'crop_id', label: 'Cultivo', tipo: 'select', lookup: 'crops', requerido: true },
			{ key: 'greenhouse_id', label: 'Invernadero', tipo: 'select', lookup: 'greenhouses', requerido: true },
			{ key: 'fecha_siembra', label: 'Fecha de siembra', tipo: 'date', requerido: true },
			{ key: 'fecha_cosecha_estimada', label: 'Cosecha estimada', tipo: 'date' },
			{ key: 'fecha_cosecha_real', label: 'Cosecha real', tipo: 'date' },
			{ key: 'cantidad_plantas', label: 'Cantidad de plantas', tipo: 'number', step: '1', min: 0 },
			{
				key: 'estado_cultivo',
				label: 'Estado del lote',
				tipo: 'select',
				opciones: ['creciendo', 'floracion', 'cosechado', 'perdido']
			},
			{ key: 'notas', label: 'Notas', tipo: 'textarea', ancho: 12 }
		]
	},
	alerts: {
		titulo: 'Alertas',
		singular: 'alerta',
		icono: 'bi-bell',
		ruta: 'alertas',
		columnas: [
			{ key: 'greenhouse_nombre', label: 'Invernadero' },
			{ key: 'tipo', label: 'Tipo', tipo: 'etiqueta' },
			{ key: 'mensaje', label: 'Mensaje' },
			{ key: 'prioridad', label: 'Prioridad', tipo: 'etiqueta' },
			{ key: 'estado_alerta', label: 'Estado', tipo: 'etiqueta' },
			{ key: 'creado', label: 'Registrada', tipo: 'fechahora' },
			{ key: 'actualizado', label: 'Actualizado', tipo: 'fechahora' }
		],
		campos: [
			{ key: 'greenhouse_id', label: 'Invernadero', tipo: 'select', lookup: 'greenhouses', requerido: true },
			{ key: 'sensor_id', label: 'Sensor (opcional)', tipo: 'select', lookup: 'sensors' },
			{ key: 'tipo', label: 'Tipo de alerta', tipo: 'text', requerido: true },
			{ key: 'prioridad', label: 'Prioridad', tipo: 'select', opciones: ['baja', 'media', 'alta'] },
			{ key: 'valor_actual', label: 'Valor actual', tipo: 'number', step: '0.01' },
			{ key: 'umbral', label: 'Umbral', tipo: 'number', step: '0.01' },
			{
				key: 'estado_alerta',
				label: 'Estado de la alerta',
				tipo: 'select',
				opciones: ['activa', 'reconocida', 'resuelta']
			},
			{ key: 'mensaje', label: 'Mensaje', tipo: 'textarea', requerido: true, ancho: 12 }
		]
	},
	irrigation_zones: {
		titulo: 'Zonas de riego',
		singular: 'zona de riego',
		icono: 'bi-droplet',
		ruta: 'zonas-riego',
		columnas: [
			{ key: 'nombre', label: 'Zona' },
			{ key: 'greenhouse_nombre', label: 'Invernadero' },
			{ key: 'tipo', label: 'Tipo de riego', tipo: 'etiqueta' },
			{ key: 'capacidad_litros_min', label: 'Litros min', tipo: 'numero' },
			{ key: 'capacidad_litros_max', label: 'Litros max', tipo: 'numero' },
			{ key: 'actualizado', label: 'Actualizado', tipo: 'fechahora' }
		],
		campos: [
			{ key: 'greenhouse_id', label: 'Invernadero', tipo: 'select', lookup: 'greenhouses', requerido: true },
			{ key: 'nombre', label: 'Nombre de la zona', tipo: 'text', requerido: true },
			{ key: 'tipo', label: 'Tipo de riego', tipo: 'select', opciones: ['gotas', 'aspersion', 'microaspersion'] },
			{ key: 'capacidad_litros_min', label: 'Capacidad minima (litros)', tipo: 'number', step: '0.01', min: 0 },
			{ key: 'capacidad_litros_max', label: 'Capacidad maxima (litros)', tipo: 'number', step: '0.01', min: 0 }
		]
	},
	irrigation_logs: {
		titulo: 'Historial de riego',
		singular: 'registro de riego',
		icono: 'bi-clock-history',
		ruta: 'historial-riego',
		columnas: [
			{ key: 'zone_nombre', label: 'Zona de riego' },
			{ key: 'duracion_minutos', label: 'Duracion (min)', tipo: 'numero' },
			{ key: 'cantidad_agua_litros', label: 'Agua (litros)', tipo: 'numero' },
			{ key: 'modo', label: 'Modo', tipo: 'etiqueta' },
			{ key: 'resultado', label: 'Resultado', tipo: 'etiqueta' },
			{ key: 'creado', label: 'Registrado', tipo: 'fechahora' },
			{ key: 'actualizado', label: 'Actualizado', tipo: 'fechahora' }
		],
		campos: [
			{ key: 'zone_id', label: 'Zona de riego', tipo: 'select', lookup: 'zones', requerido: true },
			{ key: 'duracion_minutos', label: 'Duracion (minutos)', tipo: 'number', step: '1', min: 1, requerido: true },
			{ key: 'cantidad_agua_litros', label: 'Agua utilizada (litros)', tipo: 'number', step: '0.01', min: 0 },
			{ key: 'modo', label: 'Modo', tipo: 'select', opciones: ['automatico', 'manual'] },
			{ key: 'resultado', label: 'Resultado', tipo: 'select', opciones: ['exitoso', 'parcial', 'fallido'] },
			{ key: 'notas', label: 'Notas', tipo: 'textarea', ancho: 12 }
		]
	},
	actuators: {
		titulo: 'Actuadores',
		singular: 'actuador',
		icono: 'bi-fan',
		ruta: 'actuadores',
		columnas: [
			{ key: 'nombre', label: 'Actuador' },
			{ key: 'tipo', label: 'Tipo', tipo: 'etiqueta' },
			{ key: 'greenhouse_nombre', label: 'Invernadero' },
			{ key: 'ubicacion', label: 'Ubicacion' },
			{ key: 'estado_actuador', label: 'Funcionamiento', tipo: 'etiqueta' },
			{ key: 'actualizado', label: 'Actualizado', tipo: 'fechahora' }
		],
		campos: [
			{ key: 'greenhouse_id', label: 'Invernadero', tipo: 'select', lookup: 'greenhouses', requerido: true },
			{
				key: 'tipo',
				label: 'Tipo de actuador',
				tipo: 'select',
				opciones: ['ventana', 'ventilador', 'bomba_agua', 'luz_artificial'],
				requerido: true
			},
			{ key: 'nombre', label: 'Nombre', tipo: 'text', requerido: true },
			{ key: 'ubicacion', label: 'Ubicacion', tipo: 'text' },
			{ key: 'estado_actuador', label: 'Funcionamiento', tipo: 'select', opciones: ['activo', 'inactivo'] }
		]
	},
	actuator_controls: {
		titulo: 'Control de actuadores',
		singular: 'orden de control',
		icono: 'bi-toggles',
		ruta: 'control-actuadores',
		columnas: [
			{ key: 'actuator_nombre', label: 'Actuador' },
			{ key: 'accion', label: 'Accion', tipo: 'etiqueta' },
			{ key: 'valor_ajuste', label: 'Ajuste' },
			{ key: 'resultado', label: 'Resultado', tipo: 'etiqueta' },
			{ key: 'usuario_username', label: 'Ejecutado por' },
			{ key: 'creado', label: 'Fecha', tipo: 'fechahora' },
			{ key: 'actualizado', label: 'Actualizado', tipo: 'fechahora' }
		],
		automaticos: { usuario_id: 'userId' },
		campos: [
			{ key: 'actuator_id', label: 'Actuador', tipo: 'select', lookup: 'actuators', requerido: true },
			{
				key: 'accion',
				label: 'Accion',
				tipo: 'select',
				opciones: ['abrir', 'cerrar', 'encender', 'apagar', 'ajustar'],
				requerido: true
			},
			{ key: 'valor_ajuste', label: 'Valor del ajuste (ej. 60%)', tipo: 'text' },
			{ key: 'resultado', label: 'Resultado', tipo: 'select', opciones: ['exitoso', 'fallido'] }
		]
	},
	greenhouse_settings: {
		titulo: 'Parametros del invernadero',
		singular: 'parametro',
		icono: 'bi-sliders',
		ruta: 'parametros',
		claveId: 'greenhouse_id',
		columnas: [
			{ key: 'greenhouse_nombre', label: 'Invernadero' },
			{ key: 'temp_min', label: 'T min (°C)', tipo: 'numero' },
			{ key: 'temp_max', label: 'T max (°C)', tipo: 'numero' },
			{ key: 'humedad_min', label: 'Hum. min (%)', tipo: 'numero' },
			{ key: 'humedad_max', label: 'Hum. max (%)', tipo: 'numero' },
			{ key: 'ph_min', label: 'pH min', tipo: 'numero' },
			{ key: 'ph_max', label: 'pH max', tipo: 'numero' },
			{ key: 'intervalo_lectura_minutos', label: 'Lectura cada (min)', tipo: 'numero' },
			{ key: 'actualizado', label: 'Actualizado', tipo: 'fechahora' }
		],
		campos: [
			{ key: 'greenhouse_id', label: 'Invernadero', tipo: 'select', lookup: 'greenhouses', requerido: true, soloCrear: true },
			{ key: 'temp_min', label: 'Temperatura minima (°C)', tipo: 'number', step: '0.1' },
			{ key: 'temp_max', label: 'Temperatura maxima (°C)', tipo: 'number', step: '0.1' },
			{ key: 'humedad_min', label: 'Humedad minima (%)', tipo: 'number', step: '0.1' },
			{ key: 'humedad_max', label: 'Humedad maxima (%)', tipo: 'number', step: '0.1' },
			{ key: 'luz_min', label: 'Luz minima (lux)', tipo: 'number', step: '1' },
			{ key: 'ph_min', label: 'pH minimo', tipo: 'number', step: '0.1' },
			{ key: 'ph_max', label: 'pH maximo', tipo: 'number', step: '0.1' },
			{ key: 'intervalo_lectura_minutos', label: 'Intervalo de lectura (min)', tipo: 'number', step: '1', min: 1 }
		]
	},
	usuario: {
		titulo: 'Usuarios',
		singular: 'usuario',
		icono: 'bi-people',
		ruta: 'usuarios',
		columnas: [
			{ key: 'nombre', label: 'Nombre' },
			{ key: 'username', label: 'Usuario' },
			{ key: 'email', label: 'Correo' },
			{ key: 'rol_id', label: 'Rol', lookup: 'roles', tipo: 'etiqueta' },
			{ key: 'creado', label: 'Creado', tipo: 'fechahora' }
		],
		campos: [
			{ key: 'nombre', label: 'Nombre completo', tipo: 'text', requerido: true },
			{ key: 'username', label: 'Usuario', tipo: 'text', requerido: true },
			{ key: 'email', label: 'Correo electronico', tipo: 'email', requerido: true },
			{ key: 'rol_id', label: 'Rol', tipo: 'select', lookup: 'roles', requerido: true },
			{
				key: 'password',
				label: 'Contrasena',
				tipo: 'password',
				requeridoAlCrear: true,
				ayuda: 'Al editar, deja vacio para conservar la actual.'
			}
		]
	},
	sensores_externos: {
		titulo: 'Sensores externos',
		singular: 'sensor externo',
		icono: 'bi-cloud-sun',
		ruta: 'sensores-externos',
		columnas: [
			{ key: 'ubicacion', label: 'Estacion' },
			{ key: 'tipo', label: 'Variable', tipo: 'etiqueta' },
			{ key: 'valor_actual', label: 'Valor actual', tipo: 'numero' },
			{ key: 'actualizado', label: 'Actualizado', tipo: 'fechahora' }
		],
		campos: [
			{ key: 'ubicacion', label: 'Estacion o ubicacion', tipo: 'text', requerido: true },
			{
				key: 'tipo',
				label: 'Variable que mide',
				tipo: 'select',
				opciones: ['temperatura', 'precipitacion', 'viento', 'humedad', 'radiacion'],
				requerido: true
			},
			{ key: 'valor_actual', label: 'Valor actual', tipo: 'number', step: '0.01' }
		]
	},
	lecturas_externas: {
		titulo: 'Lecturas externas',
		singular: 'lectura externa',
		icono: 'bi-clipboard-data',
		ruta: 'lecturas-externas',
		columnas: [
			{ key: 'sensor_id', label: 'Estacion', lookup: 'sensoresExternos' },
			{ key: 'valor', label: 'Valor', tipo: 'numero' },
			{ key: 'timestamp', label: 'Fecha de la lectura', tipo: 'fechahora' },
			{ key: 'actualizado', label: 'Actualizado', tipo: 'fechahora' }
		],
		campos: [
			{ key: 'sensor_id', label: 'Estacion', tipo: 'select', lookup: 'sensoresExternos', requerido: true },
			{ key: 'valor', label: 'Valor medido', tipo: 'number', step: '0.01', requerido: true },
			{ key: 'timestamp', label: 'Fecha y hora', tipo: 'datetime-local' }
		]
	},
	alertas_externas: {
		titulo: 'Alertas externas',
		singular: 'alerta externa',
		icono: 'bi-cloud-lightning-rain',
		ruta: 'alertas-externas',
		columnas: [
			{ key: 'mensaje', label: 'Mensaje' },
			{ key: 'prioridad', label: 'Prioridad', tipo: 'etiqueta' },
			{ key: 'creado', label: 'Registrada', tipo: 'fechahora' },
			{ key: 'actualizado', label: 'Actualizado', tipo: 'fechahora' }
		],
		campos: [
			{ key: 'prioridad', label: 'Prioridad', tipo: 'select', opciones: ['baja', 'media', 'alta'], requerido: true },
			{ key: 'mensaje', label: 'Mensaje', tipo: 'textarea', requerido: true, ancho: 12 }
		]
	}
};

export const rutaDe = (nombre) => {
	const modulos = (MODULOS);
	return modulos[nombre] ? '/' + modulos[nombre].ruta : null;
};
