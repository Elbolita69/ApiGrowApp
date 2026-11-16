// DEPRECADO: la capa de servicios es `src/lib/services/` (un archivo por dominio).
// Este archivo queda solo como re-export para no romper imports antiguos:
// usa `#lib/services/index.js` o el archivo del dominio (ej. `#lib/services/crops.js`).
export { request, BASE_FASTAPI, BASE_EXPRESS } from './services/api.js';
export * as servicios from './services/index.js';
