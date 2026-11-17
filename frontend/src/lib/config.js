const URL_FASTAPI = (import.meta.env.VITE_API_URL || '').replace(/\/$/, '');
const URL_EXPRESS = (import.meta.env.VITE_EXPRESS_URL || '').replace(/\/$/, '');

export const BASE_FASTAPI = URL_FASTAPI || '/api';
export const BASE_EXPRESS = URL_EXPRESS || '/api-express';
