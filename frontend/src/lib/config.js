// URLs de las APIs. Se cambian con variables de entorno de Vite:
//   VITE_API_URL      -> API principal (FastAPI + PostgreSQL)
//   VITE_EXPRESS_URL  -> API auxiliar (Express + MySQL)
// Local: http://localhost:8000 y http://localhost:3000. Nube: las URLs de Render (ver .env.example).
export const API_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '');
export const EXPRESS_URL = (import.meta.env.VITE_EXPRESS_URL || 'http://localhost:3000').replace(
	/\/$/,
	''
);
