// Configuracion del cliente. Todas las llamadas a la API pasan por el proxy de Vite
// (ver vite.config.js), nunca por una URL absoluta desde el navegador:
//   /api         -> API principal  (FastAPI + PostgreSQL)
//   /api-express -> API auxiliar  (Express + MySQL)
// El destino real se cambia sin tocar codigo con las variables de entorno
// VITE_API_TARGET y VITE_EXPRESS_TARGET del proceso de Vite.
//
// En desarrollo el proxy de Vite resuelve esos prefijos. Al publicar el
// frontend como sitio estatico no hay proxy: por eso VITE_API_URL y
// VITE_EXPRESS_URL permiten apuntar a las URLs publicas de las APIs. Si
// estan definidas ganan sobre el proxy; si no, se usa el prefijo relativo.

/** @type {string} */
const URL_FASTAPI = (import.meta.env.VITE_API_URL || '').replace(/\/$/, '');
/** @type {string} */
const URL_EXPRESS = (import.meta.env.VITE_EXPRESS_URL || '').replace(/\/$/, '');

// Base de la API principal: la URL publica si se define, si no el proxy local.
export const BASE_FASTAPI = URL_FASTAPI || '/api';
// Base de la API auxiliar: la URL publica si se define, si no el proxy local.
export const BASE_EXPRESS = URL_EXPRESS || '/api-express';
